import threading
import time

import pyautogui
import keyboard
import random
from utils import *


def goToInventorySpot(client, string_dict, lock_dict, inventory_table, item):
    row = 0
    column = 0
    while row <= 6:
        while column <= 3:
            if inventory_table[row][column].get() == item:
                print(f"Found {item} in inv ( {row}, {column} )")
                moveMouse(getTRNVCoord(client.table_inventory_rects[row][column]))
                row = 9
                column = 9
            column += 1
        row += 1
        column = 0


def readPotions(client, string_dict, lock_dict, inventory_table):

    if 'Drink' not in string_dict['absorption'].get():
        with lock_dict['absorption']:
            if pixelMatchesColor(getColor((28, 88,)), color_white, tolerance=2)\
                    and pixelMatchesColor(getColor((28, 101,)), color_white, tolerance=2):
                string_dict['absorption'].set('1**')
            elif pixelMatchesColor(getColor((28, 92,)), color_white, tolerance=2):
                string_dict['absorption'].set('2**')
            elif pixelMatchesColor(getColor((28, 99,)), color_white, tolerance=2):
                string_dict['absorption'].set('3**')
            else:
                string_dict['absorption'].set('???')

    if 'Drink' not in string_dict['buff'].get():
        with lock_dict['buff']:
            # Checks if buff is in double digits still
            current_pixel = 123
            previous_color = 0
            green_lines = 0
            while current_pixel <= 141:
                current_color = getColor((current_pixel, 346,))
                if pixelMatchesColor(current_color, color_green, tolerance=2) and decimalColortoRGB(previous_color) != color_green:
                    green_lines += 1
                previous_color = current_color
                current_pixel += 1

            if green_lines == 2:
                string_dict['buff'].set('>=10 remaining')
            elif green_lines == 1:
                string_dict['buff'].set('<=9 remaining')
            else:
                string_dict['buff'].set('Unknown')

    if string_dict['absorption'].get() == '2**' or string_dict['absorption'].get() == '1**':
        threading.Thread(target=drinkAbsorption,
                         args=(client, string_dict, lock_dict, inventory_table),
                         daemon=True).start()

    if string_dict['buff'].get() == '<=9 remaining':
        threading.Thread(target=drinkBuff,
                         args=(client, string_dict, lock_dict, inventory_table),
                         daemon=True).start()


def drinkBuff(client, string_dict, lock_dict, inventory_table):
    sleep_duration = round(getSleepTRNV(60))
    with lock_dict['buff']:
        for timer in range(sleep_duration):
            string_dict['buff'].set(f"{timer}/{sleep_duration} Waiting to Drink.")
            time.sleep(1)
        string_dict['buff'].set("Waiting on other movement to finish.")

    with lock_dict['movement']:
        with lock_dict['buff']:
            string_dict['buff'].set("Drinking.")
        moveToTab(client, "Items")
        time.sleep(getSleepTRNV(1))
        goToInventorySpot(client, string_dict, lock_dict, inventory_table, "S")
        time.sleep(getSleepTRNV(.5))
        pyautogui.click()
        time.sleep(getSleepTRNV(.05))
        moveOffScreen(client)
        string_dict['buff'].set("Done.")


def drinkAbsorption(client, string_dict, lock_dict, inventory_table):
    sleep_duration = round(getSleepTRNV(70))
    with lock_dict['absorption']:
        for timer in range(sleep_duration):
            string_dict['absorption'].set(f"{timer}/{sleep_duration} Waiting to Drink.")
            time.sleep(1)
        string_dict['absorption'].set("Waiting on other movement to finish.")

    with lock_dict['movement']:
        with lock_dict['absorption']:
            string_dict['absorption'].set("Drinking.")
            moveToTab(client, "Items")
            time.sleep(getSleepTRNV(1.3))
            goToInventorySpot(client, string_dict, lock_dict, inventory_table, "A")
            time.sleep(getSleepTRNV(.5))
            for i in range(round(getTRNV(14, 12, 16))):
                pyautogui.click()
                time.sleep(getSleepTRNV(.05))
            moveOffScreen(client)
    string_dict['absorption'].set("Done.")


def readInventory(client, string_dict, lock_dict, inventory_table):
    item_tab_color = getColor(coord_item_tab_check)
    prayer_tab_color = getColor(coord_prayer_tab_check)
    if pixelMatchesColor(item_tab_color, color_tab_selected, tolerance=10):
        client.tab = 'Items'
        string_dict['inventory'].set('On items tab.')

    elif pixelMatchesColor(prayer_tab_color, color_tab_selected, tolerance=10):
        client.tab = 'Prayer'
        string_dict['inventory'].set('On prayer tab.')
    else:
        client.tab = 'Unknown'
        string_dict['inventory'].set('On unknown tab.')

    if client.tab == 'Items':
        one_dose = coord_inv_slot1_1[1]
        for row in range(7):
            x = coord_inv_slot1_1[0]
            for column in range(4):
                color_array = [
                    getColor((x, one_dose,)),
                    getColor((x, one_dose-7,)),
                    getColor((x, one_dose-10,)),
                    getColor((x, one_dose-12,))
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

    client.update()  # WARNING - IS UPDATING CLIENT EVERY SECOND


def readHealth(client):
    if pixelMatchesColor(getColor(coord_health_check_1), color_health_is_present, tolerance=10)\
            and pixelMatchesColor(getColor(coord_health_check_2,), color_health_is_present, tolerance=10)\
            and not pixelMatchesColor(getColor(coord_health_false_check,), color_health_is_present, tolerance=10):
        client.health = '1'
        return '1 hp'
    else:
        client.health = 'Unknown'
        return '? hp'


def NMZ(client, string_dict, lock_dict, inventory_table):

    with lock_dict['status']:
        string_dict['status'].set('NMZ Started.')

    client.setFocus()

    while True:
        # Set Rapid Heal coords.
        coords = getTRNVCoord(client.rect_rapid_heal)

        # Check health and start rock cake thread if necessary.
        if client.health != '1' and client.eating == 'Pending':
            threading.Thread(target=eatRockCake,
                             args=(client, string_dict, lock_dict, inventory_table),
                             daemon=True).start()

        with lock_dict['status']:
            string_dict['status'].set("Flicking Rapid.")

        with lock_dict['movement']:

            # Go to prayer tab if necessary
            moveToTab(client, 'Prayer')

            # Move to Rapid Heal coords.
            moveMouse(coords)
            time.sleep(getSleepTRNV(.2))

            # Flick rapid heal.
            pyautogui.click()
            time.sleep(getSleepTRNV(.4))
            pyautogui.click()

        # Move mouse off screen and click

        if client.eating == 'Pending':
            with lock_dict['movement']:
                with lock_dict['status']:
                    string_dict['status'].set("Moving cursor off screen.")
                moveOffScreen(client)

        # Start waiting 1 minute before flicking rapid heal
        sleep_duration = round(getSleepTRNV(55))
        with lock_dict['status']:
            for timer in range(sleep_duration):
                string_dict['status'].set(f"{timer}/{sleep_duration - 1} Waiting to flick Rapid Heal.")
                time.sleep(1)


def moveOffScreen(client):  # Must have movement lock in calling function to call
    moveMouse((client.rectangle.right + 10, client.rectangle.top + getSleepTRNV(300),))
    time.sleep(getSleepTRNV(.3))
    pyautogui.click()


def moveToTab(client, tab):  # Only call with movement lock.
    rect = client.rect_prayer_tab
    f_key = 'f3'
    if tab == 'Prayer':
        rect = client.rect_prayer_tab
        f_key = 'f3'
    elif tab == 'Items':
        rect = client.rect_inventory_tab
        f_key = 'f2'
    if client.tab != tab:
        if random.randint(0, 1) == 2: # Turned off F keys, need focus on runelite
            pyautogui.press(f_key)
            time.sleep(getSleepTRNV(.27))
        else:
            moveMouse(getTRNVCoord(rect))
            time.sleep(getSleepTRNV(.4))
            pyautogui.click()
            time.sleep(getSleepTRNV(.3))


def eatRockCake(client, string_dict, lock_dict, inventory_table):
    print("In eat rock cake.")
    client.eating = 'Eating'

    with lock_dict['health']:
        print("Have lock in eat rock cake.")
        # Wait for timer to eat rock cake.
        sleep_duration = round(getSleepTRNV(5))
        for timer in range(sleep_duration):
            string_dict['health'].set(f"{timer}/{sleep_duration} Waiting to guzzle rock cake.")
            time.sleep(1)

        string_dict['health'].set("Guzzling rock cake now.")

        moveToTab(client, 'Items')

        goToInventorySpot(client, string_dict, lock_dict, inventory_table, '(*)')
        time.sleep(getSleepTRNV(.2))
        pyautogui.rightClick()
        time.sleep(getSleepTRNV(.4))
        x, y = pyautogui.position()
        moveMouse((getTRNV(x, x-5, x+5), getTRNV(y+41, y+36, y+46),))
        time.sleep(getSleepTRNV(.2))
        pyautogui.click()
        time.sleep(getSleepTRNV(.4))
        client.eating = 'Pending'
        moveOffScreen(client)


def login(client):  # Takes control of the mouse and keyboard to login to Runelite.
    print('Beginning login script.')
    readPassword()
    client.update()
    client.setFocus()
    current_color = getColor(coord_login_box_check)
    if pixelMatchesColor(current_color, color_user_box_is_present, tolerance=10):
        print("Clicking \"Existing user\" box.")
        moveMouse(client.coord_existing_user)
        time.sleep(getSleepTRNV(.4))
        pyautogui.click()
        time.sleep(getSleepTRNV(1))
    moveMouse(client.coord_login_entry)
    time.sleep(getSleepTRNV(.2))
    pyautogui.click()
    time.sleep(getSleepTRNV(.2))
    pyautogui.keyDown('ctrl')
    pyautogui.press('v')
    pyautogui.keyUp('ctrl')
    print('Logged in.')


def autoAlch(client, string_var, lock):
    client.setFocus()
    time.sleep(.5)
    pyautogui.press('f4')
    time.sleep(.5)
    # Set Clicking Rectangle
    firstCoords = [client.getX(.8751545117), client.getY(.3464419476)]
    secondCoords = [client.getX(.8936959209), client.getY(.3164794007)]
    clickrectangle = firstCoords + secondCoords
    # Set Smelter
    smelterPOS = [round(client.rectangle.left + (client.client_width * .8294190358)),
                  round(client.rectangle.bottom - (client.client_height * .3689138577))]
    print(str(smelterPOS))
    smelterColor = pyautogui.pixel(smelterPOS[0], smelterPOS[1])
    print(str(smelterPOS) + " Mouse position")
    print(str(smelterColor) + " Pixel color")
    with lock:
        string_var.set("Auto-Alching")
    client.update()
    randominterval = 1
    quitCounter = 0
    pyautogui.press('f4')
    newx = random.normalvariate(((clickrectangle[2] - clickrectangle[0]) / 2) + clickrectangle[0], 1.848448998)
    newy = random.normalvariate(((clickrectangle[3] - clickrectangle[1]) / 2) + clickrectangle[1], 1.599684449)
    pyautogui.moveTo(newx, newy, 1, pyautogui.easeOutQuad)
    pyautogui.click(interval=randominterval)
    pyautogui.press('f4')
    print("Starting auto alch")
    while True:
        if keyboard.is_pressed('esc'):
            break
        if pyautogui.pixelMatchesColor(smelterPOS[0], smelterPOS[1], smelterColor, tolerance=2):
            quitCounter = 0
        elif (quitCounter > 10):
            break
        if random.randrange(1, 6) == 1:
            newx = random.normalvariate(((clickrectangle[2] - clickrectangle[0]) / 2) + clickrectangle[0], 1.848448998)
            newy = random.normalvariate(((clickrectangle[3] - clickrectangle[1]) / 2) + clickrectangle[1], 1.599684449)
            print("{} , {}".format(newx, newy))
            # pyautogui.moveTo(random.randrange(clickrectangle[0], clickrectangle[2]),random.randrange(clickrectangle[1], clickrectangle[3]), 1, pyautogui.easeOutQuad)
            pyautogui.moveTo(newx, newy, 1, pyautogui.easeOutQuad)
            print("Adjusting click location.")
        if random.randrange(1, 10) == 1:
            randominterval = random.uniform(0.8, 1.2)
            print("Adjusting click interval.")

        quitCounter = quitCounter + 1

        pyautogui.click(interval=randominterval)
        if pyautogui.pixelMatchesColor(smelterPOS[0], smelterPOS[1], smelterColor, tolerance=2):
            quitCounter = 0
    with lock:
        string_var.set("Auto-Alching stopped.")
