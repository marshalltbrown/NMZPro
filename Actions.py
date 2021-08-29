import threading
import pyautogui
import random
import keyboard
from utils import *


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


def NMZ(client, status_var, health_var, lock, health_lock):
    client.setFocus()
    status_var.set('NMZ Started.')
    newx = random.normalvariate(((client.getX(0.9060568603213844) - client.getX(0.8726823238566132)) / 2) + client.getX(0.8726823238566132), 5.247710123)
    newy = random.normalvariate(((client.getY(0.4250936329588015) - client.getY(0.4737827715355805)) / 2) + client.getY(0.4737827715355805), 4.446260313)
    with lock:
        if client.tab != 'prayer':
            pyautogui.press('f3')
        generateMousePlot((newx, newy,))
    while True:
        if client.health != '1' and client.eating == 'Pending':
            client.eating = 'Eating'
            newx = random.normalvariate(((client.getX(0.9060568603213844) - client.getX(0.8726823238566132)) / 2) + client.getX(0.8726823238566132), 5.247710123)
            newy = random.normalvariate(((client.getY(0.4250936329588015) - client.getY(0.4737827715355805)) / 2) + client.getY(0.4737827715355805), 4.446260313)
            threading.Thread(target=eatRockCake, args=(client, health_var, lock, health_lock,), daemon=True).start()
        with lock:
            client.setFocus()
            status_var.set("Flicking Rapid Heal now.")
            generateMousePlot((newx, newy,))
            if random.randrange(1, 4) == 1:
                newx = random.normalvariate(((client.getX(0.9060568603213844) - client.getX(0.8726823238566132)) / 2) + client.getX(0.8726823238566132), 5.247710123)
                newy = random.normalvariate(((client.getY(0.4250936329588015) - client.getY(0.4737827715355805)) / 2) + client.getY(0.4737827715355805), 4.446260313)
            if client.tab != 'prayer':
                pyautogui.press('f3')
            pyautogui.click()
            time.sleep(random.normalvariate(.5, .15))
            pyautogui.click()
            if random.randrange(1, 6) == 1:
                newx = random.normalvariate(((client.getX(0.9060568603213844) - client.getX(0.8726823238566132)) / 2) + client.getX(0.8726823238566132), 5.247710123)
                newy = random.normalvariate(((client.getY(0.4250936329588015) - client.getY(0.4737827715355805)) / 2) + client.getY(0.4737827715355805), 4.446260313)
                generateMousePlot((newx, newy,))
        sleep_duration = round(random.normalvariate(56, 5))
        for timer in range(sleep_duration):
            status_var.set(f"{timer}/{sleep_duration - 1} Waiting to flick Rapid Heal.")
            time.sleep(1)


def eatRockCake(client, health_var, lock, health_lock):
    newx = random.normalvariate(((client.getX(0.7342398022249691) - client.getX(0.7058096415327565)) / 2) + client.getX(0.7058096415327565),3.947710123)
    newy = random.normalvariate(((client.getY(0.5) - client.getY(0.5430711610486891)) / 2) + client.getY(0.5430711610486891),3.146260313)
    print(f"newx: {newx}\nnewy: {newy}")
    with health_lock:
        sleep_duration = round(random.normalvariate(30, 5))
        for timer in range(sleep_duration):
            health_var.set(f"{timer}/{sleep_duration} Waiting to guzzle rock cake.")
            time.sleep(1)
        health_var.set("Guzzling rock cake now.")
        with lock:
            client.setFocus()
            pyautogui.press('f2')
            time.sleep(random.normalvariate(.8, .1))
            pyautogui.moveTo(newx, newy, (random.normalvariate(.6, .06)), pyautogui.easeOutQuad)
            pyautogui.rightClick()
            time.sleep(random.normalvariate(.7, .1))
            newx = newx + random.normalvariate(0, 2.5)
            newy = newy + random.normalvariate(45, .1)
            pyautogui.moveTo(newx, newy, (random.normalvariate(.4, .012)), pyautogui.easeOutQuad)
            time.sleep(random.normalvariate(.6, .221))
            pyautogui.click()
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
        time.sleep(random.normalvariate(.5, .1))
    generateMousePlot(client.coord_login_entry)
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
