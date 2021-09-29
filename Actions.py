import sys
import threading

import keyboard
import pyautogui
import win32ui

from utils import *


def testt(client, script):
    invent = client.get_items('A')
    if len(invent) > 3:
        invent = invent[:3]
    if len(invent) != 0:
        for i in range(len(invent)):
            moveMouse(invent[i])
            time.sleep(.3)


def NMZ(client, script):
    mouse = Controller()
    flick_time_threshold = time.time()
    absorb_threshold = getTRNV(250, 180, 300)

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

        if client.hp > 1 and (rock := client.get_items('(*)')):
            eatRockCake(client, script, rock)

        if time.time() >= flick_time_threshold:
            flickRapidHeal(client, script)
            flick_time_threshold = time.time() + getSleepTRNV(57)

        if client.absorbs <= absorb_threshold and (pots := client.get_items('A')):
            drinkAbsorption(client, script, pots)
            absorb_threshold = getTRNV(250, 180, 300)

        if not client.buffed and (pots := client.get_items(client.style)):
            drinkBuff(client, script, pots)

        x, y = mouse.position
        if client.rectangle.left < x < client.rectangle.right \
                and client.rectangle.top < y < client.rectangle.bottom:
            moveOffScreen(client, script)

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
                        overload_pots = client.get_items('O')
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


def drinkBuff(client, script, buffs) -> None:  # Done

    with script.lock:

        script.post("Drinking buff pot.")

        # Move to tab
        moveToTab(client, "Items")
        time.sleep(getSleepTRNV(1))

        # Move to 1st buff pot
        moveMouse(buffs[0])
        time.sleep(getSleepTRNV(.5))

        # Click buff pot
        pyautogui.click()
        time.sleep(getSleepTRNV(.1))

        script.post("Buff pot drank.")


def drinkAbsorption(client, script, pots) -> None:  # Done

    with script.lock:

        script.post("Drinking absorption pot.")

        # Move to tab
        moveToTab(client, "Items")
        time.sleep(getSleepTRNV(.3))

        # Limits pots to click to 3
        if len(pots) > 3:
            pots = pots[:3]

        # Loop to move to first 3 absorbs and drink each of them
        for i in range(len(pots)):  # Moves to absorb
            moveMouse(pots[i])
            time.sleep(.3)
            for _ in range(round(getTRNV(15, 13, 17))):  # Clicks absorb pot a psuedo random number of times.
                pyautogui.click()
                time.sleep(getSleepTRNV(.05))

        script.post("Absorb pot drank.")

        time.sleep(getSleepTRNV(.1))


def flickRapidHeal(client, script) -> None:  # Done

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

        # Move to prayer location. ( Either quick pray or actual rapid heal )
        moveMouse(coords)
        time.sleep(getSleepTRNV(.15))

        # Flick ( Double click) prayer location. ( Either quick pray or actual rapid heal )
        pyautogui.click()
        time.sleep(getSleepTRNV(.6))
        pyautogui.click()
        time.sleep(getSleepTRNV(.15))


def eatRockCake(client, script, rock) -> None:  # Done

    with script.lock:

        script.post("Guzzling rock cake.")

        # Move to tab
        moveToTab(client, "Items")
        time.sleep(getSleepTRNV(.3))

        # Move to rock cake
        moveMouse(rock[0])
        time.sleep(getSleepTRNV(.1))

        # Right click to bring up guzzle menu
        pyautogui.rightClick()
        time.sleep(getSleepTRNV(.2))

        # Move mouse down relative to current location to reach "Guzzle" menu option
        x, y = pyautogui.position()
        moveMouse((getTRNV(x, x - 5, x + 5), getTRNV(y + 41, y + 36, y + 46),))
        time.sleep(getSleepTRNV(.2))

        # Click to finish guzzling rock cake
        pyautogui.click()
        time.sleep(getSleepTRNV(.1))


def logout(client, script) -> None:

    # Simple wait to look a bit more human
    time.sleep(getSleepTRNV(20))

    script.post("Logging out.")

    with script.lock:

        # Move to logout tab
        moveToTab(client, 'Logout')
        time.sleep(getSleepTRNV(.2))

        # Move mouse to logout button
        moveMouse(getTRNVCoord(client.rect_logout_button))
        time.sleep(getSleepTRNV(.1))

        # Click logout button TODO: See if a double click is needed here
        pyautogui.click()
        time.sleep(getSleepTRNV(.1))
        pyautogui.click()
        time.sleep(getSleepTRNV(.1))


def moveOffScreen(client, script) -> None:
    with script.lock:

        # Moves the mouse just off the right side of the Runelite client
        moveMouse((client.rectangle.right + 10, client.rectangle.top + getSleepTRNV(300),))
        time.sleep(getSleepTRNV(.3))

        # Click off screen to be sure Runelite loses window focus
        pyautogui.click()
        time.sleep(getSleepTRNV(.2))


def moveToTab(client, tab) -> None:
    # TODO: Actually implement random chance to change using f-key (Runelite needs focus)
    # TODO: Use enums instead of strings. Try to include f-key and rect data.
    f_key = ''

    if tab == 'Items':
        rect = client.rect_inventory_tab
        f_key = 'f2'
    elif tab == 'Logout':
        rect = client.rect_logout_tab
        # No F key for logging out
    else:
        rect = client.rect_prayer_tab
        f_key = 'f3'

    if client.tab != tab:  # If not already on the desired tab
        if random.randint(0, 1) == 100:  # Currently never returns True. Runelite needs focus for f_key to do anything.
            # Presses f key to change tabs
            pyautogui.press(f_key)
            time.sleep(getSleepTRNV(.27))
        else:  # Currently always falls to this
            # Move to tab change region
            moveMouse(getTRNVCoord(rect))
            time.sleep(getSleepTRNV(.08))

            # Clicks the tab to finish changing tabs
            pyautogui.click()
            time.sleep(getSleepTRNV(.08))


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
