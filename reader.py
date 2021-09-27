import threading

import cv2
import win32ui
from PIL import Image
import numpy as np
from utils import *
import pyautogui
from easyocr import Reader


def reader(client, sentinel):
    mouse = Controller()
    window = win32ui.FindWindow(None, "RuneLite")
    ocr = Reader(['en'], gpu=True)
    while sentinel.active:
        checkMovement(client, window)
        dc = window.GetWindowDC()
        try:
            readTab(client, sentinel, dc)
            if sentinel.style == 'O':
                readOverloadState(client, sentinel, dc)
            else:
                readBuffPot(client, sentinel, dc)
            if sentinel.style == 'O':
                read_buff_2(client, sentinel, ocr)
            else:
                read_buff_1(client, sentinel, ocr)
            readHealth(client, sentinel, ocr)
            pos = mouse.position
            if pos[0] >= client.rectangle.right or pos[1] <= 207+client.rectangle.top:
                readInventory(client, sentinel.inv_strings, dc)
            dc.DeleteDC()
        except Exception as e:
            print(e)
        client.absorbs_remaining = countPots(sentinel.inv_strings, 'A')
        client.buffs_remaining = countPots(sentinel.inv_strings, sentinel.style)
        time.sleep(.3)


def checkMovement(client, window):
    r = window.GetWindowRect()
    top_left = (r[0], r[1],)
    bottom_right = (r[2], r[3],)
    if top_left != client.offset:
        print('Updated client')
        client.update(top_left, bottom_right)


def readOverloadState(client, sentinel, dc): #TODO set timer and track 5 mins from overload click
    pass


def checkNMZ(dc):  # Checks 2 pixels on a Runelite display absorption pot while in NMZ (top-left of screen)
    if pixelMatchesColor(dc.GetPixel(40, 80), (144, 136, 123,), tolerance=10)\
            and pixelMatchesColor(dc.GetPixel(47, 75), (132, 116, 49,), tolerance=10):
        return True
    else:
        return False


def countPots(inventory_table, pot):
    pot_found = False
    for row in range(7):
        for column in range(4):
            if pot in inventory_table[row][column].get():
                pot_found = True
    return pot_found


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
                    inv_strings[row][column].set('(*)')
                elif (itemCheck(color_array, color_empty_potion, 8)) == 4:
                    inv_strings[row][column].set('X')
                elif (result := itemCheck(color_array, color_range_potion, 30)) != 0:
                    inv_strings[row][column].set(f"R{result}")
                elif (result := itemCheck(color_array, color_absorption_pot, 15)) != 0:
                    inv_strings[row][column].set(f"A{result}")
                elif (result := itemCheck(color_array, color_strength_pot, 15)) != 0:
                    inv_strings[row][column].set(f"S{result}")
                elif (result := itemCheck(color_array, color_overload_pot, 10)) != 0:
                    inv_strings[row][column].set(f"O{result}")
                elif (itemCheck(color_array, color_inv_empty, 15)) == 4:
                    inv_strings[row][column].set('-')
                else:
                    inv_strings[row][column].set('?')
                x += 42
            one_dose += 36


def readTab(client, sentinel, dc):
    item_tab_color = dc.GetPixel(*coord_item_tab_check)
    prayer_tab_color = dc.GetPixel(*coord_prayer_tab_check)

    if pixelMatchesColor(item_tab_color, color_tab_selected, tolerance=10):
        client.tab = 'Items'
        sentinel.strings['inventory'].set('On items tab.')

    elif pixelMatchesColor(prayer_tab_color, color_tab_selected, tolerance=10):
        client.tab = 'Prayer'
        sentinel.strings['inventory'].set('On prayer tab.')
    else:
        client.tab = 'Unknown'
        sentinel.strings['inventory'].set('On unknown tab.')


def readBuffPot(client, sentinel, dc):
    if not sentinel.drinking_buff:
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
            sentinel.strings['buff'].set('>=10 remaining')
            client.buffed = True
        elif green_lines == 1:
            sentinel.strings['buff'].set('<=9 remaining')
            client.buffed = False
        else:
            sentinel.strings['buff'].set('???')
            client.buffed = False


def resize_image(image):
    basewidth = 75
    wpercent = (basewidth / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    img = image.resize((basewidth, hsize), Image.ANTIALIAS)
    return img


def read_buff_1(client, sentinel, ocr):
    left = 27 + client.rectangle.left
    top = 95 + client.rectangle.top
    width = 29
    height = 12
    absorb_region = (left, top, width, height,)
    img = pyautogui.screenshot(region=absorb_region)
    img = resize_image(img)
    img = np.array(img)
    word = ocr.readtext(img, allowlist='0123456789', detail=0)
    if len(word) != 0:
        client.inNMZ = True
        word = word[0]
        if not sentinel.drinking_absorbs:
            sentinel.strings['absorption'].set(f"{word} Remaining")
        client.absorbs = int(word)
    else:
        client.inNMZ = False


def read_buff_2(client, sentinel, ocr):
    left = 90 + client.rectangle.left
    top = 95 + client.rectangle.top
    width = 29
    height = 12
    absorb_region = (left, top, width, height,)
    img = pyautogui.screenshot(region=absorb_region)
    img = resize_image(img)
    img = np.array(img)
    word = ocr.readtext(img, allowlist='0123456789', detail=0)
    if len(word) != 0:
        client.inNMZ = True
        word = word[0]
        if not sentinel.drinking_absorbs:
            sentinel.strings['absorption'].set(f"{word} Remaining")
        client.absorbs = int(word)
    else:
        client.inNMZ = False


def readHealth(client, sentinel, ocr):
    left = 524 + client.rectangle.left
    top = 82 + client.rectangle.top
    width = 545 - 524
    height = 95 - 82
    hp_region = (left, top, width, height,)

    low_thresh = (60, 160, 160)
    high_thresh = (255, 260, 260)

    img = pyautogui.screenshot(region=hp_region)
    img = np.array(resize_image(img))

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, low_thresh, high_thresh)
    blur = cv2.GaussianBlur(mask, (7, 7), 0)
    word = ocr.readtext(blur, allowlist='0123456789', detail=0)

    if len(word) != 0:
        word = word[0]
        sentinel.strings['health'].set(f"{word} hp")
        client.hp = int(word)


