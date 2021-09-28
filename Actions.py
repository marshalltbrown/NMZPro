import sys
import threading

import keyboard
import pyautogui
import win32ui

from utils import *


def testt(client, script):
    invent = getInventoryLocations(client, script, 'A')
    if len(invent) > 3:
        invent = invent[:3]
    if len(invent) != 0:
        for i in range(len(invent)):
            moveMouse(invent[i])
            time.sleep(.3)


def NMZ(client, script):

    while True:
        if not client.inNMZ:
            timer = 0
            while timer <= 10:
                if client.inNMZ:
                    continue
                if timer == 10:
                    script.active = False
                    script.post("NMZ not found.")
                    time.sleep(getSleepTRNV(3))
                    logout(client, script)
                    sys.exit()
                time.sleep(1)
                timer += 1

        if not script.drinking_absorbs and client.check_pot('A') and client.absorbs <= 250:
            threading.Thread(target=drinkAbsorption, args=(client, script), daemon=True).start()

        if not script.drinking_buff and client.check_pot(script.style) and not client.buffed:
            threading.Thread(target=drinkBuff, args=(client, script), daemon=True).start()

        if not script.eating and client.hp > 1:
            threading.Thread(target=eatRockCake, args=(client, script), daemon=True).start()

        if not script.flicking:
            threading.Thread(target=flickRapidHeal, args=(client, script), daemon=True).start()

        time.sleep(1)


def overload(client, script):
    while True:
        if not client.inNMZ:
            timer = 0
            while timer <= 10:
                if client.inNMZ:
                    continue
                if timer == 10:
                    script.active = False
                    script.post("NMZ not found.")
                    time.sleep(getSleepTRNV(3))
                    logout(client, script)
                    sys.exit()
                time.sleep(1)
                timer += 1

        if script.overload_time_left <= 45 and client.check_pot('O'):
            script.overloading = True
            threading.Thread(target=flickRapidHeal, args=(client, script), kwargs={'sleep_time': .1}, daemon=True).start()
            if not script.eating and client.hp > 1:
                threading.Thread(target=eatRockCake, args=(client, script), kwargs={'sleep_time': .1}, daemon=True).start()
            if not script.drinking_absorbs and client.check_pot('A') and client.absorbs <= 250:
                threading.Thread(target=drinkAbsorption, args=(client, script), kwargs={'sleep_time': .1}, daemon=True).start()
            in_place = False
            while time_left := script.overload_time_left <= 45:
                with script.lock:
                    if 15 <= time_left <= 25 and not in_place:
                        moveToTab(client, "Prayer")
                        time.sleep(getSleepTRNV(.2))
                        moveMouse(getTRNVCoord(client.rect_melee_prayer))
                    if time_left <= 1:
                        pyautogui.click()
                        moveToTab(client, "Items")
                        overload_pots = getInventoryLocations(client, script, 'O')
                        if len(overload_pots) != 0:
                            moveMouse(overload_pots[0])
                            time.sleep(getSleepTRNV(.15))
                            pyautogui.click()

                            while not script.overloaded:
                                time.sleep(getSleepTRNV(.05))
                                pyautogui.click()
                            time.sleep(getSleepTRNV(.3))
                            moveToTab(client, "Prayer")
                            time.sleep(getSleepTRNV(.2))
                            moveMouse(getTRNVCoord(client.rect_melee_prayer))
                            pyautogui.click()
                            moveOffScreen(client, script)
                        else:
                            script.overloading = False
                            continue

        if not script.flicking and not script.overloading:
            threading.Thread(target=flickRapidHeal, args=(client, script), daemon=True).start()

        if not script.drinking_absorbs and client.check_pot('A') and client.absorbs <= 250\
                and not script.overloading:
            threading.Thread(target=drinkAbsorption, args=(client, script), daemon=True).start()

        if not script.drinking_buff and client.check_pot('O') and not client.buffed and not script.overloading:
            threading.Thread(target=drinkBuff, args=(client, script), daemon=True).start()

        if not script.eating and client.hp > 1 and not script.overloading:
            threading.Thread(target=eatRockCake, args=(client, script), daemon=True).start()


def drinkBuff(client, script, sleep_time=60):
    script.drinking_buff = True
    sleep_duration = round(getSleepTRNV(sleep_time))
    for timer in range(sleep_duration):
        if not script.active:
            script.drinking_buff = False
            sys.exit()
        if timer > (sleep_duration - 5):
            script.moving_soon['buff'] = True
        script.strings['buff'].set(f"{timer}/{sleep_duration} Waiting to drink.")
        time.sleep(1)

    script.moving_soon['buff'] = False
    while script.check_moving_soon():
        time.sleep(.3)

    script.strings['buff'].set("Waiting on other movement.")
    with script.lock:
        script.strings['buff'].set("Drinking.")
        script.post("Drinking buff pot.")
        moveToTab(client, "Items")
        time.sleep(getSleepTRNV(1))
        buffs = getInventoryLocations(client, script, script.style)
        if len(buffs) != 0:
            moveMouse(buffs[0])
            time.sleep(getSleepTRNV(.5))
            pyautogui.click()
            time.sleep(getSleepTRNV(.05))
        else:
            script.drinking_buff = False
            sys.exit()
    if not script.overloading:
        moveOffScreen(client, script)
    script.drinking_buff = False


def drinkAbsorption(client, script, sleep_time=70):
    script.drinking_absorbs = True
    sleep_duration = round(getSleepTRNV(sleep_time))
    for timer in range(sleep_duration):
        if not script.active:
            script.drinking_absorbs = False
            sys.exit()
        if timer > (sleep_duration - 5):
            script.moving_soon['absorb'] = True
        script.strings['absorption'].set(f"{timer}/{sleep_duration} Waiting to drink.")
        time.sleep(1)

    script.moving_soon['absorb'] = False
    while script.check_moving_soon():
        time.sleep(.3)

    script.strings['absorption'].set("Waiting.")
    with script.lock:
        script.post("Drinking absorption pot.")
        moveToTab(client, "Items")
        time.sleep(getSleepTRNV(.3))
        absorbs = getInventoryLocations(client, script, "A")  # Gets list of absorbs
        if len(absorbs) > 3:  # Drinks up to 3 absorbs
            absorbs = absorbs[:3]
        if len(absorbs) != 0:
            for i in range(len(absorbs)):  # Moves to absorb
                moveMouse(absorbs[i])
                time.sleep(.3)
                for _1 in range(round(getTRNV(15, 13, 17))):  # Clicks absorb pot
                    pyautogui.click()
                    time.sleep(getSleepTRNV(.05))
            else:
                script.drinking_absorbs = False
                sys.exit()
        time.sleep(getSleepTRNV(.5))
    if not script.overloading:
        moveOffScreen(client, script)
    script.drinking_absorbs = False


def flickRapidHeal(client, script, sleep_time=52):
    script.flicking = True
    # Start waiting ~1 minute before flicking rapid heal
    sleep_duration = round(getSleepTRNV(sleep_time))
    for timer in range(sleep_duration):
        if not script.active:
            script.flicking = False
            sys.exit()
        if timer > (sleep_duration - 5):
            script.moving_soon['flicking'] = True
        script.strings['status'].set(f"{timer}/{sleep_duration - 1} Waiting to flick.")
        time.sleep(1)

    script.moving_soon['flicking'] = False
    while script.check_moving_soon():
        time.sleep(.3)

    with script.lock:
        # Small chance to go directly to prayer tab
        if random.randrange(1, 10) == 1:
            script.post("Moving to prayer tab to flick. (1/10 odds)")
            # Set rapid heal rect
            coords = getTRNVCoord(client.rect_rapid_heal)
            # Go to prayer tab if necessary
            moveToTab(client, 'Prayer')
            time.sleep(getSleepTRNV(.15))
        else:
            # Set quick pray rect.
            coords = getTRNVCoord(client.rect_quick_pray)

        script.post("Flicking rapid heal now.")
        # Move to prayer spot.
        moveMouse(coords)
        time.sleep(getSleepTRNV(.15))

        # Flick prayer.
        pyautogui.click()
        time.sleep(getSleepTRNV(.6))
        pyautogui.click()

        # Move off screen
        time.sleep(getSleepTRNV(.15))
    if not script.overloading:
        moveOffScreen(client, script)
    script.flicking = False


def eatRockCake(client, script, sleep_time=.3):
    script.eating = True
    # Wait for timer to eat rock cake.
    sleep_duration = round(getSleepTRNV(sleep_time))
    for timer in range(sleep_duration):
        if not script.active:
            script.eating = False
            sys.exit()
        if timer > (sleep_duration - 5):
            script.moving_soon['eating'] = True
        script.strings['health'].set(f"{timer}/{sleep_duration} Waiting to guzzle rock cake.")
        time.sleep(1)

    script.moving_soon['eating'] = False
    while script.check_moving_soon():
        time.sleep(.3)

    with script.lock:
        script.post("Guzzling rock cake.")

        moveToTab(client, 'Items')
        time.sleep(getSleepTRNV(.1))
        rock = getInventoryLocations(client, script, '(*)')
        if len(rock) != 0:
            moveMouse(rock[0])
            time.sleep(getSleepTRNV(.1))
            pyautogui.rightClick()
            time.sleep(getSleepTRNV(.2))
            x, y = pyautogui.position()
            moveMouse((getTRNV(x, x - 5, x + 5), getTRNV(y + 41, y + 36, y + 46),))
            time.sleep(getSleepTRNV(.1))
            pyautogui.click()
            time.sleep(getSleepTRNV(.2))
        else:
            script.eating = False
            sys.exit()
    if not script.overloading:
        moveOffScreen(client, script)
    script.eating = False


def logout(client, script):
    time.sleep(getSleepTRNV(10))
    with script.lock:
        script.post("Logging out.")
        moveToTab(client, 'Logout')
        time.sleep(getSleepTRNV(.2))
        moveMouse(getTRNVCoord(client.rect_logout_button))
        time.sleep(getSleepTRNV(.1))
        pyautogui.click()
        time.sleep(getSleepTRNV(.1))
        pyautogui.click()
        moveOffScreen(client, script)


def getInventoryLocations(client, script, item):
    inventory = []
    for row in range(7):
        for column in range(4):
            if item in script.inv_strings[row][column].get():
                inventory.append(getTRNVCoord(client.inventory[row][column].rect))

    return inventory


def moveOffScreen(client, script):  # Must have movement lock in calling function to call
    if not script.lock.locked():
        with script.lock:
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


def login(client, script):  # Takes control of the mouse and keyboard to login to Runelite.
    script.post('Beginning login script.')
    readPassword()
    client.setFocus()
    window = win32ui.FindWindow(None, "RuneLite")
    dc = window.GetWindowDC()
    current_color = dc.GetPixel(*coord_login_box_check)
    if pixelMatchesColor(current_color, color_user_box_is_present, tolerance=10):
        script.post("Clicking \"Existing user\" box.")
        moveMouse(client.coord_existing_user)
        time.sleep(getSleepTRNV(.4))
        pyautogui.click()
        time.sleep(getSleepTRNV(1))
    moveMouse(client.coord_login_entry)
    time.sleep(getSleepTRNV(.2))
    pyautogui.click()
    time.sleep(getSleepTRNV(.2))
    script.post('Pasting saved password.')
    pyautogui.keyDown('ctrl')
    pyautogui.press('v')
    pyautogui.keyUp('ctrl')
    script.post('Ready to log in.')


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
