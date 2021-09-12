import win32ui
from utils import *
from pynput.mouse import Controller


def reader(client, string_dict, inventory_table):
    mouse = Controller()
    while True:
        client.update()
        window = win32ui.FindWindow(None, "RuneLite")
        dc = window.GetWindowDC()
        try:
            readTab(client, string_dict, dc)
            readBuffPot(client, string_dict, dc)
            readAbsorbPot(client, string_dict, dc)
            readHealth(client, string_dict, dc)
            pos = mouse.position
            if pos[0] >= client.rectangle.right or (231 + client.rectangle.top <= pos[1] <= 239 + client.rectangle.top)\
                    or pos[1] <= 207+client.rectangle.top:
                readInventory(client, inventory_table, dc)
            client.inNMZ = checkNMZ(dc)
            dc.DeleteDC()
        except:
            print("Window error.")
        client.absorbs_remaining = countPots(inventory_table, 'A')
        client.buffs_remaining = countPots(inventory_table, client.training_style)
        time.sleep(.3)


def checkNMZ(dc):
    if pixelMatchesColor(dc.GetPixel(40, 80), (144, 136, 123,), tolerance=5)\
            and pixelMatchesColor(dc.GetPixel(47, 75), (132, 116, 49,), tolerance=5):
        return True
    else:
        return False


def countPots(inventory_table, pot):
    pot_found = False
    for row in range(7):
        for column in range(4):
            if inventory_table[row][column].get() == pot:
                pot_found = True
    return pot_found


def readInventory(client, inventory_table, dc):
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
                    inventory_table[row][column].set('(*)')
                elif (itemCheck(color_array, color_empty_potion, 8)) == 4:
                    inventory_table[row][column].set('0')
                elif (result := itemCheck(color_array, color_range_potion, 30)) != 0:
                    inventory_table[row][column].set("R")
                elif (result := itemCheck(color_array, color_absorption_pot, 15)) != 0:
                    inventory_table[row][column].set("A")
                elif (result := itemCheck(color_array, color_strength_pot, 15)) != 0:
                    inventory_table[row][column].set("S")
                elif (itemCheck(color_array, color_inv_empty, 15)) == 4:
                    inventory_table[row][column].set('-')
                else:
                    inventory_table[row][column].set('  ?  ')
                x += 42
            one_dose += 36


def readTab(client, string_dict, dc):
    item_tab_color = dc.GetPixel(*coord_item_tab_check)
    prayer_tab_color = dc.GetPixel(*coord_prayer_tab_check)

    if pixelMatchesColor(item_tab_color, color_tab_selected, tolerance=10):
        client.tab = 'Items'
        string_dict['inventory'].set('On items tab.')

    elif pixelMatchesColor(prayer_tab_color, color_tab_selected, tolerance=10):
        client.tab = 'Prayer'
        string_dict['inventory'].set('On prayer tab.')
    else:
        client.tab = 'Unknown'
        string_dict['inventory'].set('On unknown tab.')


def readBuffPot(client, string_dict, dc):
    if client.buff == 'Pending':
        # Checks if buff is in double digits still
        current_pixel = 123
        previous_color = 0
        green_lines = 0
        while current_pixel <= 141:
            current_color = dc.GetPixel(current_pixel, 346)
            if pixelMatchesColor(current_color, color_green, tolerance=2) and decimalColortoRGB(
                    previous_color) != color_green:
                green_lines += 1
            previous_color = current_color
            current_pixel += 1

        if green_lines == 2:
            string_dict['buff'].set('>=10 remaining')
        elif green_lines == 1:
            string_dict['buff'].set('<=9 remaining')
        else:
            string_dict['buff'].set('???')


def readAbsorbPot(client, string_dict, dc):
    if client.absorption == 'Pending':
        if pixelMatchesColor(dc.GetPixel(28, 88), color_white, tolerance=2) \
                and pixelMatchesColor(dc.GetPixel(28, 101), color_white, tolerance=2):
            string_dict['absorption'].set('100+')
        elif pixelMatchesColor(dc.GetPixel(28, 92), color_white, tolerance=2):
            string_dict['absorption'].set('200+')
        elif pixelMatchesColor(dc.GetPixel(28, 99), color_white, tolerance=2):
            string_dict['absorption'].set('300+')
        else:
            string_dict['absorption'].set('???')


def readHealth(client, string_dict, dc):
    if client.eating == 'Pending':
        if pixelMatchesColor(dc.GetPixel(*coord_health_check_1), color_health_is_present, tolerance=10) \
                and pixelMatchesColor(dc.GetPixel(*coord_health_check_2), color_health_is_present, tolerance=10) \
                and not pixelMatchesColor(dc.GetPixel(*coord_health_false_check), color_health_is_present, tolerance=10):
            string_dict['health'].set('1 HP')
        else:
            string_dict['health'].set('? HP')

