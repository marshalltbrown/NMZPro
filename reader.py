import threading
import cv2
import win32ui
from PIL import Image
import numpy as np
from pywinauto import Application

from utils import *
import pyautogui
from easyocr import Reader


def overload_tracker(client, script):
    timer = time.time()
    location = (client.rectangle.left, client.rectangle.top, client.rectangle.right, client.rectangle.bottom)
    script.overloaded = read_overload(pyautogui.screenshot(region=location))
    while script.active:
        try:
            # Get window DC used for getting color from pixels
            if read_overload(pyautogui.screenshot(region=location)) and not script.overloaded:
                script.overloaded = True
                timer = time.time()
                while read_overload(pyautogui.screenshot(region=location)):
                    script.overload_time_left = round(300 - (time.time() - timer))
                    script.strings['buff'].set(f"{script.overload_time_left} seconds of O left")
                    time.sleep(.5)
                script.overloaded = False
                script.overload_time_left = 300
                script.strings['buff'].set("Waiting for overload.")
        except Exception as e:
            print(e)


def read_overload(im):
    top_pot = im.getpixel((40, 69,))
    mid_pot = im.getpixel((40, 83,))
    bottom_pot = im.getpixel((40, 92,))
    top = pixelMatchesColor(top_pot, (162, 145, 62,), tolerance=5)
    mid = pixelMatchesColor(mid_pot, (9, 7, 7,), tolerance=5)
    bottom = pixelMatchesColor(bottom_pot, (9, 7, 7,), tolerance=5)
    if top and mid and bottom:
        return True
    else:
        return False


def reader(client, script):
    mouse = Controller()
    window = win32ui.FindWindow(None, "RuneLite")
    ocr = Reader(['en'], gpu=True)
    
    # Params are ( left, top, width, height )
    left_pot_region = (27 + client.rectangle.left, 95 + client.rectangle.top, 29, 12,)
    right_pot_region = (90 + client.rectangle.left, 95 + client.rectangle.top, 29, 12,)

    while script.active:
        try:
            # Get window DC used for getting color from pixels
            dc = window.GetWindowDC()
            
            # Check if the window has moved. If so, update client rectangles
            client.update_location()
            
            # Reads between 3 useful tabs to see which is active
            readTab(client, script, dc)
            
            # If in overload mode, absorptions are on the box to the left
            if script.style == 'O':
                if script.overloaded:
                    read_nmz_pot(client, script, ocr, right_pot_region)
                else:
                    read_nmz_pot(client, script, ocr, left_pot_region)

            else:  # If in regular mode, absorptions are on the left
                readBuffPot(client, script, dc)
                read_nmz_pot(client, script, ocr, left_pot_region)

            # OCR health
            readHealth(client, script, ocr)

            # If mouse is not in the inventory window then read the inventory
            pos = mouse.position
            if pos[0] >= client.rectangle.right or pos[1] <= 207+client.rectangle.top:
                readInventory(client, script.inv_strings, dc)

            # Delete the DC to refresh for next run and prevent memory leaks
            dc.DeleteDC()
            
        except Exception as e:
            print(e)
        time.sleep(.3)


def readOverloadState(client, script, dc):  # TODO set timer and track 5 minutes from overload click
    pass


def readInventory(client, inv_strings, dc):
    if client.tab == 'Items':
        one_dose = coord_inv_slot1_1[1]
        for row in range(7):
            x = coord_inv_slot1_1[0]
            for column in range(4):
                color_array = [
                    dc.GetPixel(x, one_dose),
                    dc.GetPixel(x, one_dose - 7),
                    dc.GetPixel(x, one_dose - 10),
                    dc.GetPixel(x, one_dose - 12)
                ]
                if itemCheck(color_array, color_dwarven_rock, 10) == 4:
                    update_inventory(client, inv_strings, row, column, '(*)')
                elif (itemCheck(color_array, color_empty_potion, 8)) == 4:
                    update_inventory(client, inv_strings, row, column, 'X')
                elif (result := itemCheck(color_array, color_range_potion, 30)) != 0:
                    update_inventory(client, inv_strings, row, column, "R", dose=result)
                elif (result := itemCheck(color_array, color_absorption_pot, 15)) != 0:
                    update_inventory(client, inv_strings, row, column, "A", dose=result)
                elif (result := itemCheck(color_array, color_strength_pot, 15)) != 0:
                    update_inventory(client, inv_strings, row, column, "S", dose=result)
                elif (result := itemCheck(color_array, color_overload_pot, 10)) != 0:
                    update_inventory(client, inv_strings, row, column, "O", dose=result)
                elif (itemCheck(color_array, color_inv_empty, 15)) == 4:
                    update_inventory(client, inv_strings, row, column, '-')
                else:
                    update_inventory(client, inv_strings, row, column, '?')
                x += 42
            one_dose += 36


def update_inventory(client, inv_strings, row, column, contents, dose=0):
    if dose == 0:
        inv_strings[row][column].set(contents)
    else:
        inv_strings[row][column].set(f"{contents}{dose}")
    client.inventory[row][column].contents = contents


def readTab(client, script, dc):
    item_tab_color = dc.GetPixel(*coord_item_tab_check)
    prayer_tab_color = dc.GetPixel(*coord_prayer_tab_check)

    if pixelMatchesColor(item_tab_color, color_tab_selected, tolerance=10):
        client.tab = 'Items'
        script.strings['inventory'].set('On items tab.')

    elif pixelMatchesColor(prayer_tab_color, color_tab_selected, tolerance=10):
        client.tab = 'Prayer'
        script.strings['inventory'].set('On prayer tab.')
    else:
        client.tab = 'Unknown'
        script.strings['inventory'].set('On unknown tab.')


def readBuffPot(client, script, dc):
    if not script.drinking_buff:
        # Checks if buff is in double digits still
        current_pixel = 123
        previous_color = 0
        green_lines = 0
        while current_pixel <= 141:
            current_color = dc.GetPixel(current_pixel, 346)
            if pixelMatchesColor(current_color, color_green, tolerance=5) and decimalColortoRGB(
                    previous_color) != color_green:
                green_lines += 1
            previous_color = current_color
            current_pixel += 1

        if green_lines == 2:
            script.strings['buff'].set('>=10 remaining')
            client.buffed = True
        elif green_lines == 1:
            script.strings['buff'].set('<=9 remaining')
            client.buffed = False
        else:
            script.strings['buff'].set('???')
            client.buffed = False


def process_image(img, resize=False):
    if resize:
        base_width = 75
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), Image.ANTIALIAS)
    img = np.array(img)
    return img


def read_nmz_pot(client, script, ocr, pot_region):
    img = pyautogui.screenshot(region=pot_region)
    img = process_image(img, resize=True)
    word = ocr.readtext(img, allowlist='0123456789', detail=0)

    if word:
        client.inNMZ = True
        word = word[0]
        if not script.drinking_absorbs:
            script.strings['absorption'].set(f"{word} Remaining")
        client.absorbs = int(word)
    else:
        client.inNMZ = False


def readHealth(client, script, ocr):
    left = 524 + client.rectangle.left
    top = 82 + client.rectangle.top
    # Params are ( left, top, width, height )
    hp_region = (left, top, 21, 13,)

    # Thresholds to isolate health text in HSV color space
    low_thresh = (60, 160, 160)
    high_thresh = (255, 260, 260)

    img = pyautogui.screenshot(region=hp_region)
    img = process_image(img, resize=True)

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, low_thresh, high_thresh)
    blur = cv2.GaussianBlur(mask, (7, 7), 0)
    ocr_hp = ocr.readtext(blur, allowlist='0123456789', detail=0)

    if ocr_hp:
        ocr_hp = ocr_hp[0]
        script.strings['health'].set(f"{ocr_hp} hp")
        client.hp = int(ocr_hp)
