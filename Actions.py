import sys
import threading

import keyboard
import pyautogui
import win32ui

from utils import *


def NMZ(client, string_dict, lock, inventory_table):
    client.nmz_running = True
    postStatus(string_dict, "NMZ Script Started.")

    client.setFocus()

    while True:
        if not client.inNMZ:
            postStatus(string_dict, "NMZ not found.")
            client.nmz_running = False
            time.sleep(getSleepTRNV(3))
            logout(client, string_dict, lock)
            sys.exit()

        if client.absorption == 'Pending' and client.absorbs_remaining:
            if '200+' in string_dict['absorption'].get() or '100+' in string_dict['absorption'].get(): # modified instead of hard code from reader none left code
                threading.Thread(target=drinkAbsorption,
                                 args=(client, string_dict, lock, inventory_table),
                                 daemon=True).start()

        if client.buff == 'Pending' and client.buffs_remaining:
            if '>=10 remaining' not in string_dict['buff'].get():
                threading.Thread(target=drinkBuff,
                                 args=(client, string_dict, lock, inventory_table),
                                 daemon=True).start()

        # Check health and start rock cake thread if necessary.
        if client.eating == 'Pending':
            if string_dict['health'].get() == '? HP':
                threading.Thread(target=eatRockCake,
                                 args=(client, string_dict, lock, inventory_table),
                                 daemon=True).start()

        if not client.flicking:
            threading.Thread(target=flickRapidHeal,
                             args=(client, string_dict, lock),
                             daemon=True).start()
        time.sleep(1)


def postStatus(strings, message):
    box = strings['box']
    fully_scrolled_down = box.yview()[1] == 1.0

    box.insert('end', message + "\n")
    if fully_scrolled_down:
        box.see("end")


def logout(client, strings, lock):
    time.sleep(getSleepTRNV(10))
    with lock:
        postStatus(strings, "Logging out.")
        moveToTab(client, 'Logout')
        time.sleep(getSleepTRNV(.2))
        moveMouse(getTRNVCoord(client.rect_logout_button))
        time.sleep(getSleepTRNV(.1))
        pyautogui.click()
        time.sleep(getSleepTRNV(.1))
        pyautogui.click()
        moveOffScreen(client)


def goToInventorySpot(client, string_dict, lock, inventory_table, item):
    row = 0
    column = 0
    item_found = False
    while row <= 6:
        while column <= 3:
            if inventory_table[row][column].get() == item:
                moveMouse(getTRNVCoord(client.inventory[row][column].rect))
                item_found = True
                row = 9
                column = 9
            column += 1
        row += 1
        column = 0
    return item_found


def drinkBuff(client, string_dict, lock, inventory_table):

    client.buff = 'Drinking'
    sleep_duration = round(getSleepTRNV(60))
    for timer in range(sleep_duration):
        if not client.nmz_running:
            sys.exit()
        string_dict['buff'].set(f"{timer}/{sleep_duration} Waiting to drink.")
        time.sleep(1)

    string_dict['buff'].set("Waiting on other movement.")
    with lock:
        string_dict['buff'].set("Drinking.")
        postStatus(string_dict, "Drinking buff pot.")
        moveToTab(client, "Items")
        time.sleep(getSleepTRNV(1))
        if not goToInventorySpot(client, string_dict, lock, inventory_table, client.training_style):
            client.buff = 'Pending'
            sys.exit()
        time.sleep(getSleepTRNV(.5))
        pyautogui.click()
        time.sleep(getSleepTRNV(.05))
    if not lock.locked():
        with lock:
            moveOffScreen(client)
            time.sleep(getSleepTRNV(.2))
    string_dict['buff'].set("Done.")
    client.buff = 'Pending'


def drinkAbsorption(client, string_dict, lock, inventory_table):

    client.absorption = 'Drinking'

    sleep_duration = round(getSleepTRNV(70))
    for timer in range(sleep_duration):
        if not client.nmz_running:
            sys.exit()
        string_dict['absorption'].set(f"{timer}/{sleep_duration} Waiting to drink.")
        time.sleep(1)

    string_dict['absorption'].set("Waiting.")
    with lock:
        string_dict['absorption'].set("Drinking.")
        postStatus(string_dict, "Drinking absorption pot.")
        moveToTab(client, "Items")
        time.sleep(getSleepTRNV(.3))
        if not goToInventorySpot(client, string_dict, lock, inventory_table, "A"):
            client.absorption = 'Pending'
            sys.exit()
        time.sleep(getSleepTRNV(.5))
        for i in range(round(getTRNV(15, 13, 17))):
            pyautogui.click()
            time.sleep(getSleepTRNV(.05))
    if not lock.locked():
        with lock:
            moveOffScreen(client)
            time.sleep(getSleepTRNV(.2))

    string_dict['absorption'].set("Done.")
    client.absorption = 'Pending'


def flickRapidHeal(client, string_dict, lock):
    client.flicking = True
    # Start waiting ~1 minute before flicking rapid heal
    sleep_duration = round(getSleepTRNV(52))
    for timer in range(sleep_duration):
        if not client.nmz_running:
            sys.exit()
        string_dict['status'].set(f"{timer}/{sleep_duration - 1} Waiting to flick.")
        time.sleep(1)

    with lock:
        # Small chance to go directly to prayer tab
        if random.randrange(1, 10) == 1:
            postStatus(string_dict, "Moving to prayer tab to flick. (1/10 odds)")
            # Set rapid heal rect
            coords = getTRNVCoord(client.rect_rapid_heal)
            # Go to prayer tab if necessary
            moveToTab(client, 'Prayer')
            time.sleep(getSleepTRNV(.15))
        else:
            # Set quick pray rect.
            coords = getTRNVCoord(client.rect_quick_pray)

        postStatus(string_dict, "Flicking rapid heal now.")
        # Move to prayer spot.
        moveMouse(coords)
        time.sleep(getSleepTRNV(.15))

        # Flick prayer.
        pyautogui.click()
        time.sleep(getSleepTRNV(.6))
        pyautogui.click()

        # Move off screen
        time.sleep(getSleepTRNV(.15))
    if not lock.locked():
        with lock:
            moveOffScreen(client)
            time.sleep(getSleepTRNV(.2))
    client.flicking = False


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
    elif tab == 'Logout':
        rect = client.rect_logout_tab
    if client.tab != tab:
        if random.randint(0, 1) == 2:  # Turned off F keys, need focus on runelite
            pyautogui.press(f_key)
            time.sleep(getSleepTRNV(.27))
        else:  # currently always false to this
            moveMouse(getTRNVCoord(rect))
            time.sleep(getSleepTRNV(.01))
            pyautogui.click()


def eatRockCake(client, string_dict, lock, inventory_table):
    client.eating = 'Eating'
    # Wait for timer to eat rock cake.
    sleep_duration = round(getSleepTRNV(.1))
    for timer in range(sleep_duration):
        if not client.nmz_running:
            sys.exit()
        string_dict['health'].set(f"{timer}/{sleep_duration} Waiting to guzzle rock cake.")
        time.sleep(1)

    string_dict['health'].set("Guzzling rock cake now.")

    with lock:
        postStatus(string_dict, "Guzzling rock cake.")
        window = win32ui.FindWindow(None, "RuneLite")
        dc = window.GetWindowDC()
        hp_is2 = False
        if pixelMatchesColor(dc.GetPixel(533, 86), color_health_is_present, tolerance=10) \
                and pixelMatchesColor(dc.GetPixel(537, 92), color_health_is_present, tolerance=10):
            hp_is2 = True

        moveToTab(client, 'Items')
        time.sleep(getSleepTRNV(.1))
        if not goToInventorySpot(client, string_dict, lock, inventory_table, '(*)'):
            client.eating = 'Pending'
            sys.exit()
        time.sleep(getSleepTRNV(.1))
        pyautogui.rightClick()
        time.sleep(getSleepTRNV(.2))
        x, y = pyautogui.position()
        moveMouse((getTRNV(x, x - 5, x + 5), getTRNV(y + 41, y + 36, y + 46),))
        time.sleep(getSleepTRNV(.1))
        pyautogui.click()
        time.sleep(getSleepTRNV(.2))

    if hp_is2 and not lock.locked():
        with lock:
            string_dict['health'].set('1 HP')
            moveOffScreen(client)
            time.sleep(getSleepTRNV(.1))
    client.eating = 'Pending'


def login(client, strings):  # Takes control of the mouse and keyboard to login to Runelite.
    postStatus(strings, 'Beginning login script.')
    readPassword()
    client.update()
    client.setFocus()
    window = win32ui.FindWindow(None, "RuneLite")
    dc = window.GetWindowDC()
    current_color = dc.GetPixel(*coord_login_box_check)
    if pixelMatchesColor(current_color, color_user_box_is_present, tolerance=10):
        postStatus(strings, "Clicking \"Existing user\" box.")
        moveMouse(client.coord_existing_user)
        time.sleep(getSleepTRNV(.4))
        pyautogui.click()
        time.sleep(getSleepTRNV(1))
    moveMouse(client.coord_login_entry)
    time.sleep(getSleepTRNV(.2))
    pyautogui.click()
    time.sleep(getSleepTRNV(.2))
    postStatus(strings, 'Pasting saved password.')
    pyautogui.keyDown('ctrl')
    pyautogui.press('v')
    pyautogui.keyUp('ctrl')
    postStatus(strings, 'Ready to log in.')


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
