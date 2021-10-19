import time
import pyautogui
import cv2
import numpy as np
from easyocr import Reader
from PIL import Image

from utilities.object_templates import tab
from utilities.utils import pixelMatchesColor, itemCheck
from utilities.vars import colors, coords
from Runelite import tabs, runelite, rects


def reader(client, script):
    ocr = Reader(['en'], gpu=True)

    print("Reader and dependencies initialized.")

    while script.active:

        # Params are ( left, top, width, height )
        left_pot_region = (27 + client.rectangle.left, 95 + client.rectangle.top, 29, 12,)
        right_pot_region = (90 + client.rectangle.left, 95 + client.rectangle.top, 29, 12,)
        # Check if the window has moved. If so, update client rectangles
        client.update_location()

        # Set Runelite screenshot rect
        rect = client.rectangle
        runelite_region = (rect.left, rect.top, (rect.right - rect.left), (rect.bottom - rect.top))
        img = pyautogui.screenshot(region=runelite_region)

        # Reads between 3 useful tabs to see which is active
        readTab(client, img)

        # If in overload mode, absorptions are on the box to the left
        if script.style == 'O':
            if verifyOverload(client, img):
                read_nmz_pot(client, ocr, right_pot_region)
            else:
                read_nmz_pot(client, ocr, left_pot_region)

        else:  # If in regular mode, absorptions are on the left
            readBuffPot(client, img)
            read_nmz_pot(client, ocr, left_pot_region)

        # OCR health
        readHealth(client, ocr)

        # If mouse is not in the inventory grid then read the inventory
        x, y = pyautogui.position()
        rect = client.rectangle
        if not (rect.left+750 > x > rect.left+560) or not (rect.bottom > y > rect.top+207):
            readInventory(client, img)

        time.sleep(.3)
        script.gui.refresh_inventory(client)


def verifyOverload(client, img) -> bool:
    pot_cork_color = img.getpixel((40, 69,))
    pot_liquid_color = img.getpixel((40, 86,))
    result = False
    if pixelMatchesColor(pot_cork_color, (162, 145, 62), tolerance=10) \
            and pixelMatchesColor(pot_liquid_color, (9, 7, 7), tolerance=10):
        client.overloaded = True
        result = True
    else:
        client.overloaded = False
    return result


def readInventory(client, img) -> None:
    if client.current_tab != tabs.inventory:
        return

    one_dose = coords.inv_slot1_1[1]
    for row in range(7):
        x = coords.inv_slot1_1[0]
        for column in range(4):
            colors.array = [
                img.getpixel((x, one_dose,)),
                img.getpixel((x, one_dose - 7,)),
                img.getpixel((x, one_dose - 10,)),
                img.getpixel((x, one_dose - 12,))
            ]
            if itemCheck(colors.array, colors.dwarven_rock, 10) == 4:
                update_pot_in_inv(client, row, column, '(*)')
            elif (itemCheck(colors.array, colors.empty_potion, 8)) == 4:
                update_pot_in_inv(client, row, column, 'X')
            elif (result := itemCheck(colors.array, colors.range_potion, 30)) != 0:
                update_pot_in_inv(client, row, column, "R", doses=result)
            elif (result := itemCheck(colors.array, colors.absorption_pot, 15)) != 0:
                update_pot_in_inv(client, row, column, "A", doses=result)
            elif (result := itemCheck(colors.array, colors.strength_pot, 15)) != 0:
                update_pot_in_inv(client, row, column, "S", doses=result)
            elif (result := itemCheck(colors.array, colors.overload_pot, 10)) != 0:
                update_pot_in_inv(client, row, column, "O", doses=result)
            elif (itemCheck(colors.array, colors.inv_empty, 15)) == 4:
                update_pot_in_inv(client, row, column, '-')
            else:
                update_pot_in_inv(client, row, column, '?')
            x += 42
        one_dose += 36


def update_pot_in_inv(client: runelite, row, column, contents, doses=0) -> None:
    client.inventory[row][column].contents = contents
    client.inventory[row][column].pot_doses = doses


def readTab(client, img) -> None:
    item_tab_color = img.getpixel(coords.item_tab_check)
    prayer_tab_color = img.getpixel(coords.prayer_tab_check)

    if pixelMatchesColor(item_tab_color, colors.tab_selected, tolerance=10):
        client.current_tab = tabs.inventory
    elif pixelMatchesColor(prayer_tab_color, colors.tab_selected, tolerance=10):
        client.current_tab = tabs.prayer
    else:
        client.current_tab = tab((0, 0,), (2, 2,))


def readBuffPot(client, img) -> None:
    # Checks if buff is in double digits still
    previous_color = 0
    green_lines = 0
    for current_pixel in range(123, 142):
        current_color = img.getpixel((current_pixel, 346,))
        if pixelMatchesColor(current_color, colors.green, tolerance=5) \
                and not pixelMatchesColor(previous_color, colors.green, tolerance=5):
            green_lines += 1

        previous_color = current_color

    # TODO: some sort of method to limit false returns while client is moved.
    if green_lines == 2:
        client.buffed = True
    else:
        client.buffed = False


def process_image(img, resize=False):
    # Default flag to enlarge the image
    if resize:
        base_width = 75  # Increases the image based off this number
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), Image.ANTIALIAS)
    # Returns np.array used for OCR
    img = np.array(img)
    return img


def read_nmz_pot(client, ocr, pot_region) -> None:
    # Get screenshot from region
    img = pyautogui.screenshot(region=pot_region)
    # Prep image for OCR
    img = process_image(img, resize=True)
    # OCR the image
    word = ocr.readtext(img, allowlist='0123456789', detail=0)

    # TODO: if the value is too far off it shouldn't register
    if word:
        client.inNMZ = True
        if len(word[0]) == 3:  # TODO: A better way to weed out wrong results?
            client.absorbs = int(word[0])
    else:
        client.inNMZ = False


def readHealth(client, ocr) -> None:
    rect = rects.hp_ocr_box
    # Params are ( left, top, width, height )
    hp_region = (rect.left, rect.top, rect.width, rect.height,)

    # Thresholds to isolate health text in HSV color space
    low_thresh = (60, 160, 160)
    high_thresh = (255, 260, 260)

    # Get screenshot from region
    img = pyautogui.screenshot(region=hp_region)
    img = process_image(img, resize=True)

    # Prep image for OCR
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, low_thresh, high_thresh)
    blur = cv2.GaussianBlur(mask, (7, 7), 0)
    ocr_hp = ocr.readtext(blur, allowlist='0123456789', detail=0)

    if ocr_hp:
        ocr_hp = ocr_hp[0]
        client.hp = int(ocr_hp)
