import threading
import win32ui
from utils import *


def reader(client, sentinel):
    mouse = Controller()
    window = win32ui.FindWindow(None, "RuneLite")
    while sentinel.active:
        checkMovement(client, window)
        dc = window.GetWindowDC()
        try:
            readTab(client, sentinel, dc)
            readBuffPot(client, sentinel, dc)
            readAbsorbPot(client, sentinel, dc)
            readHealth(client, sentinel, dc)
            pos = mouse.position
            if pos[0] >= client.rectangle.right or pos[1] <= 207+client.rectangle.top:
                readInventory(client, sentinel.inv_strings, dc)
            client.inNMZ = checkNMZ(dc)
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
                    inv_strings[row][column].set('0')
                elif (result := itemCheck(color_array, color_range_potion, 30)) != 0:
                    inv_strings[row][column].set(f"R{result}")
                elif (result := itemCheck(color_array, color_absorption_pot, 15)) != 0:
                    inv_strings[row][column].set(f"A{result}")
                elif (result := itemCheck(color_array, color_strength_pot, 15)) != 0:
                    inv_strings[row][column].set(f"S{result}")
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


def readAbsorbPot(client, sentinel, dc):
    if not sentinel.drinking_absorbs:
        if pixelMatchesColor(dc.GetPixel(28, 88), color_white, tolerance=2) \
                and pixelMatchesColor(dc.GetPixel(28, 101), color_white, tolerance=2):
            sentinel.strings['absorption'].set('100+')
            client.absorbed = False
        elif pixelMatchesColor(dc.GetPixel(28, 92), color_white, tolerance=2):
            sentinel.strings['absorption'].set('200+')
            client.absorbed = False
        elif pixelMatchesColor(dc.GetPixel(28, 99), color_white, tolerance=2):
            sentinel.strings['absorption'].set('300+')
            client.absorbed = True
        else:
            sentinel.strings['absorption'].set('???')
            client.absorbed = True


def readHealth(client, sentinel, dc):
    if not sentinel.eating:
        if pixelMatchesColor(dc.GetPixel(*coord_health_check_1), color_health_is_present, tolerance=10) \
                and pixelMatchesColor(dc.GetPixel(*coord_health_check_2), color_health_is_present, tolerance=10) \
                and not pixelMatchesColor(dc.GetPixel(*coord_health_false_check), color_health_is_present, tolerance=10):
            sentinel.strings['health'].set('1 HP')
            client.hp_is_1 = True
        else:
            sentinel.strings['health'].set('? HP')
            client.hp_is_1 = False

