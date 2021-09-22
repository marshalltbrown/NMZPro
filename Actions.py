import sys
import threading

import keyboard
import pyautogui
import win32ui

from utils import *


def testt(client, sentinel):
    while True:
        goToInventorySpot(client, sentinel, '(*)')
        time.sleep(4)


def NMZ(client, sentinel):
    client.nmz_running = True
    client.setFocus()

    while True:
        if not client.inNMZ:
            sentinel.active = client.inNMZ
            sentinel.post("NMZ not found.")
            time.sleep(getSleepTRNV(3))
            logout(client, sentinel)
            sys.exit()

        if not sentinel.drinking_absorbs and client.absorbs_remaining and not client.absorbed:
            threading.Thread(target=drinkAbsorption, args=(client, sentinel), daemon=True).start()

        if not sentinel.drinking_buff and client.buffs_remaining and not client.buffed:
            threading.Thread(target=drinkBuff, args=(client, sentinel), daemon=True).start()

        if not sentinel.eating and not client.hp_is_1:
            threading.Thread(target=eatRockCake, args=(client, sentinel), daemon=True).start()

        if not sentinel.flicking:
            threading.Thread(target=flickRapidHeal, args=(client, sentinel), daemon=True).start()

        time.sleep(1)


def drinkBuff(client, sentinel):
    sentinel.drinking_buff = True
    sleep_duration = round(getSleepTRNV(60))
    for timer in range(sleep_duration):
        if not sentinel.active:
            sentinel.drinking_buff = False
            sys.exit()
        if timer > (sleep_duration - 5):
            sentinel.moving_soon['buff'] = True
        sentinel.strings['buff'].set(f"{timer}/{sleep_duration} Waiting to drink.")
        time.sleep(1)

    sentinel.moving_soon['buff'] = False
    while sentinel.check_moving_soon():
        time.sleep(.3)

    sentinel.strings['buff'].set("Waiting on other movement.")
    with sentinel.lock:
        sentinel.strings['buff'].set("Drinking.")
        sentinel.post("Drinking buff pot.")
        moveToTab(client, "Items")
        time.sleep(getSleepTRNV(1))
        if not goToInventorySpot(client, sentinel, sentinel.training_style):
            sentinel.drinking_buff = False
            sys.exit()
        time.sleep(getSleepTRNV(.5))
        pyautogui.click()
        time.sleep(getSleepTRNV(.05))

    moveOffScreen(client, sentinel)

    sentinel.strings['buff'].set("Done.")
    sentinel.drinking_buff = False


def drinkAbsorption(client, sentinel):
    sentinel.drinking_absorbs = True
    sleep_duration = round(getSleepTRNV(70))
    for timer in range(sleep_duration):
        if not client.nmz_running:
            sentinel.drinking_absorbs = False
            sys.exit()
        if timer > (sleep_duration - 5):
            sentinel.moving_soon['absorb'] = True
        sentinel.strings['absorption'].set(f"{timer}/{sleep_duration} Waiting to drink.")
        time.sleep(1)

    sentinel.moving_soon['absorb'] = False
    while sentinel.check_moving_soon():
        time.sleep(.3)

    sentinel.strings['absorption'].set("Waiting.")
    with sentinel.lock:
        sentinel.post("Drinking absorption pot.")
        moveToTab(client, "Items")
        time.sleep(getSleepTRNV(.3))
        if not goToInventorySpot(client, sentinel, "A"):
            sentinel.drinking_absorbs = False
            sys.exit()
        time.sleep(getSleepTRNV(.5))
        for i in range(round(getTRNV(15, 13, 17))):
            pyautogui.click()
            time.sleep(getSleepTRNV(.05))
    moveOffScreen(client, sentinel)
    sentinel.drinking_absorbs = False


def flickRapidHeal(client, sentinel):
    sentinel.flicking = True
    # Start waiting ~1 minute before flicking rapid heal
    sleep_duration = round(getSleepTRNV(52))
    for timer in range(sleep_duration):
        if not client.nmz_running:
            sentinel.flicking = False
            sys.exit()
        if timer > (sleep_duration - 5):
            sentinel.moving_soon['flicking'] = True
        sentinel.strings['status'].set(f"{timer}/{sleep_duration - 1} Waiting to flick.")
        time.sleep(1)

    sentinel.moving_soon['flicking'] = False
    while sentinel.check_moving_soon():
        time.sleep(.3)

    with sentinel.lock:
        # Small chance to go directly to prayer tab
        if random.randrange(1, 10) == 1:
            sentinel.post("Moving to prayer tab to flick. (1/10 odds)")
            # Set rapid heal rect
            coords = getTRNVCoord(client.rect_rapid_heal)
            # Go to prayer tab if necessary
            moveToTab(client, 'Prayer')
            time.sleep(getSleepTRNV(.15))
        else:
            # Set quick pray rect.
            coords = getTRNVCoord(client.rect_quick_pray)

        sentinel.post("Flicking rapid heal now.")
        # Move to prayer spot.
        moveMouse(coords)
        time.sleep(getSleepTRNV(.15))

        # Flick prayer.
        pyautogui.click()
        time.sleep(getSleepTRNV(.6))
        pyautogui.click()

        # Move off screen
        time.sleep(getSleepTRNV(.15))
    moveOffScreen(client, sentinel)
    sentinel.flicking = False


def eatRockCake(client, sentinel):
    sentinel.eating = True
    # Wait for timer to eat rock cake.
    sleep_duration = round(getSleepTRNV(.1))
    for timer in range(sleep_duration):
        if not client.nmz_running:
            sentinel.eating = False
            sys.exit()
        if timer > (sleep_duration - 5):
            sentinel.moving_soon['eating'] = True
        sentinel.strings['health'].set(f"{timer}/{sleep_duration} Waiting to guzzle rock cake.")
        time.sleep(1)

    sentinel.moving_soon['eating'] = False
    while sentinel.check_moving_soon():
        time.sleep(.3)

    with sentinel.lock:
        sentinel.post("Guzzling rock cake.")
        window = win32ui.FindWindow(None, "RuneLite")
        dc = window.GetWindowDC()
        hp_is2 = False
        if pixelMatchesColor(dc.GetPixel(533, 86), color_health_is_present, tolerance=10) \
                and pixelMatchesColor(dc.GetPixel(537, 92), color_health_is_present, tolerance=10):
            hp_is2 = True

        moveToTab(client, 'Items')
        time.sleep(getSleepTRNV(.1))
        if not goToInventorySpot(client, sentinel, '(*)'):
            sentinel.eating = False
            sys.exit()
        time.sleep(getSleepTRNV(.1))
        pyautogui.rightClick()
        time.sleep(getSleepTRNV(.2))
        x, y = pyautogui.position()
        moveMouse((getTRNV(x, x - 5, x + 5), getTRNV(y + 41, y + 36, y + 46),))
        time.sleep(getSleepTRNV(.1))
        pyautogui.click()
        time.sleep(getSleepTRNV(.2))

    if hp_is2 and not sentinel.lock.locked():
        with sentinel.lock:
            sentinel.strings['health'].set('1 HP')
            client.hp_is_1 = True
            moveOffScreen(client, sentinel)
    sentinel.eating = False


def logout(client, sentinel):
    time.sleep(getSleepTRNV(10))
    with sentinel.lock:
        sentinel.post("Logging out.")
        moveToTab(client, 'Logout')
        time.sleep(getSleepTRNV(.2))
        moveMouse(getTRNVCoord(client.rect_logout_button))
        time.sleep(getSleepTRNV(.1))
        pyautogui.click()
        time.sleep(getSleepTRNV(.1))
        pyautogui.click()
        moveOffScreen(client, sentinel)


def goToInventorySpot(client, sentinel, item):
    row = 0
    column = 0
    item_found = False
    while row <= 6:
        while column <= 3:
            if item in sentinel.inv_strings[row][column].get():
                moveMouse(getTRNVCoord(client.inventory[row][column].rect))
                item_found = True
                row = 9
                column = 9
            column += 1
        row += 1
        column = 0
    return item_found


def moveOffScreen(client, sentinel):  # Must have movement lock in calling function to call
    if not sentinel.lock.locked():
        with sentinel.lock:
            moveMouse((client.rectangle.right + 10, client.rectangle.top + getSleepTRNV(300),))
            time.sleep(getSleepTRNV(.3))
            pyautogui.click()
            time.sleep(getSleepTRNV(.2))


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
        if random.randint(0, 1) == 2:  # Turned off F keys, would need focus on runelite
            pyautogui.press(f_key)
            time.sleep(getSleepTRNV(.27))
        else:  # currently always false to this
            moveMouse(getTRNVCoord(rect))
            time.sleep(getSleepTRNV(.01))
            pyautogui.click()


def login(client, sentinel):  # Takes control of the mouse and keyboard to login to Runelite.
    sentinel.post('Beginning login script.')
    readPassword()
    client.update()
    client.setFocus()
    window = win32ui.FindWindow(None, "RuneLite")
    dc = window.GetWindowDC()
    current_color = dc.GetPixel(*coord_login_box_check)
    if pixelMatchesColor(current_color, color_user_box_is_present, tolerance=10):
        sentinel.post("Clicking \"Existing user\" box.")
        moveMouse(client.coord_existing_user)
        time.sleep(getSleepTRNV(.4))
        pyautogui.click()
        time.sleep(getSleepTRNV(1))
    moveMouse(client.coord_login_entry)
    time.sleep(getSleepTRNV(.2))
    pyautogui.click()
    time.sleep(getSleepTRNV(.2))
    sentinel.post('Pasting saved password.')
    pyautogui.keyDown('ctrl')
    pyautogui.press('v')
    pyautogui.keyUp('ctrl')
    sentinel.post('Ready to log in.')


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
