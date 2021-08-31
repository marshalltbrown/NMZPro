import threading
import pyautogui
import random
import keyboard
from utils import *


def goToSpot(client, string_dict, lock_dict, inventory_table, item):
    for row in range(7):
        for column in range(4):
            if inventory_table[row][column].get() == item:
                generateMousePlot(getTRNVCoord(client.table_inventory_rects[row][column]))


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
                inventory_table[row][column].set(str(result))
            elif (itemCheck(color_array, color_inv_empty, 15)) == 4:
                inventory_table[row][column].set('-')
            else:
                inventory_table[row][column].set('  ?  ')
            x += 42
        one_dose += 36


def itemCheck(colors, sample, tolerance):
    counter = 0
    if pixelMatchesColor(colors[0], sample, tolerance=tolerance):
        counter += 1
    if pixelMatchesColor(colors[1], sample, tolerance=tolerance):
        counter += 1
    if pixelMatchesColor(colors[2], sample, tolerance=tolerance):
        counter += 1
    if pixelMatchesColor(colors[3], sample, tolerance=tolerance):
        counter += 1
    return counter


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
    client.setFocus()
    with lock_dict['status']:
        string_dict['status'].set('NMZ Started.')
        coords = getTRNVCoord(client.rect_rapid_heal)
        print(f"Moving too coords: {coords}")
        if client.tab != 'prayer':
            pyautogui.press('f3')
        generateMousePlot(coords)
    while True:
        if client.health != '1' and client.eating == 'Pending':
            client.eating = 'Eating'
            coords = getTRNVCoord(client.rect_rapid_heal)
            threading.Thread(target=eatRockCake, args=(client, string_dict, lock_dict, inventory_table), daemon=True).start()
        with lock_dict['status']:
            client.setFocus()
            string_dict['status'].set("Flicking Rapid Heal now.")
            generateMousePlot(coords)
            if random.randrange(1, 4) == 1:
                coords = getTRNVCoord(client.rect_rapid_heal)
            if client.tab != 'prayer':
                pyautogui.press('f3')
            pyautogui.click()
            time.sleep(random.normalvariate(.5, .15))
            pyautogui.click()
            if random.randrange(1, 6) == 1:
                coords = getTRNVCoord(client.rect_rapid_heal)
                generateMousePlot(coords)
        sleep_duration = round(getTRNV(57, 40, 66))
        for timer in range(sleep_duration):
            string_dict['status'].set(f"{timer}/{sleep_duration - 1} Waiting to flick Rapid Heal.")
            time.sleep(1)


def eatRockCake(client, string_dict, lock_dict, inventory_table):
    with lock_dict['health']:
        sleep_duration = round(random.normalvariate(30, 5))
        for timer in range(sleep_duration):
            string_dict['health'].set(f"{timer}/{sleep_duration} Waiting to guzzle rock cake.")
            time.sleep(1)
        string_dict['health'].set("Guzzling rock cake now.")
        with lock_dict['status']:
            client.setFocus()
            pyautogui.press('f2')
            time.sleep(getTRNV(.8, .5, 1.2))
            goToSpot(client, string_dict, lock_dict, inventory_table, '(*)')
            time.sleep(getTRNV(.2, .1, .3))
            pyautogui.rightClick()
            time.sleep(getTRNV(.4, .2, .6))
            #newx = newx + random.normalvariate(0, 2.5)
            #newy = newy + random.normalvariate(45, .1)
            #pyautogui.moveTo(newx, newy, (random.normalvariate(.4, .012)), pyautogui.easeOutQuad)
            #time.sleep(random.normalvariate(.6, .221))
            #pyautogui.click()
            client.eating = 'Pending'


def login(client):  # Takes control of the mouse and keyboard to login to Runelite.
    print('Beginning login script.')
    readPassword()
    client.update()
    client.setFocus()
    current_color = getColor(coord_login_box_check)
    if pixelMatchesColor(current_color, color_user_box_is_present, tolerance=10):
        print("Clicking \"Existing user\" box.")
        generateMousePlot(client.coord_existing_user)
        pyautogui.click()
        time.sleep(getTRNV(1, .6, 1.2))
    generateMousePlot(client.coord_login_entry)
    time.sleep(getTRNV(.2, .1, .3))
    pyautogui.click()
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
