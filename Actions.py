import keyboard
import pyautogui
from utilities.utils import *
from Runelite import tabs, rects
from utilities.object_templates import tab
from utilities.vars import coords, colors


def overload(client, script):
    mouse = Controller()
    sleep_thresh_seed = (55, 35, 70)
    flick_time_threshold = time.time() + getTRNV(*sleep_thresh_seed)
    absorb_threshold = round(getTRNV(250, 180, 300))
    overload_expiry_timer = 999999999999
    time.sleep(7)
    script.strings['status'].set('Active')
    script.post("Starting Script Now")
    while script.active:
        if client.overloaded:
            script.strings['buff'].set(f"Overload ends in {round(overload_expiry_timer - time.time())}")

            if overload_expiry_timer - time.time() <= 30 and (o_pot := client.get_item_locations('O')):
                print("im in here bro")
                flickRapidHeal(client, script)

                if client.absorbs <= 200 and (pots := client.get_item_locations('A')):
                    drinkAbsorption(client, script, pots[:1])
                    absorb_threshold = round(getTRNV(250, 180, 300))

                if client.hp > 1 and (rock := client.get_item_locations('(*)')):
                    eatRockCake(client, script, rock)

                moveToTab(client, tabs.prayer)
                moveMouse(rects.melee_prayer.random_coord)

                while overload_expiry_timer - time.time() >= 2:
                    script.strings['buff'].set(f"Overload ends in {round(overload_expiry_timer - time.time())}")
                    time.sleep(.1)

                pyautogui.click()

                moveToTab(client, tabs.inventory)
                moveMouse(o_pot[0])
                while client.overloaded:
                    time.sleep(.0001)

                pyautogui.click()
                overload_expiry_timer = time.time() + 299

                time.sleep(getSleepTRNV(5))

                moveToTab(client, tabs.prayer)
                moveMouse(rects.melee_prayer.random_coord)
                pyautogui.click()
                flick_time_threshold = time.time() + getTRNV(*sleep_thresh_seed)

            else:
                # print(client.current_tab != tabs.inventory)
                nmz_check(client, script)
                moved_this_loop = False
                # TODO if other scripts are run, may as well flick? human like?
                if client.hp > 1 and (rock := client.get_item_locations('(*)')):
                    eatRockCake(client, script, rock)
                    moved_this_loop = True
                    if (flick_time_threshold - time.time()) <= 20:
                        flickRapidHeal(client, script)
                        flick_time_threshold = time.time() + getTRNV(*sleep_thresh_seed)

                current_time = time.time()
                script.strings['health'].set(
                    f"{client.hp} hp | {round(flick_time_threshold - current_time)} secs until pray flick.")
                if time.time() >= flick_time_threshold:
                    flickRapidHeal(client, script)
                    flick_time_threshold = time.time() + getTRNV(*sleep_thresh_seed)
                    moved_this_loop = True

                script.strings['absorption'].set(f"{client.absorbs} | Drinking at {absorb_threshold}. ")
                if client.absorbs <= absorb_threshold and (pots := client.get_item_locations('A')):
                    drinkAbsorption(client, script, pots)
                    absorb_threshold = round(getTRNV(250, 180, 300))
                    moved_this_loop = True

                if not client.buffed and (pots := client.get_item_locations(script.style)):
                    drinkBuff(client, script, pots)
                    moved_this_loop = True

                x, y = mouse.position
                if client.rectangle.left < x < client.rectangle.right \
                        and client.rectangle.top < y < client.rectangle.bottom and moved_this_loop:
                    moveOffScreen(client, script)

        elif client.get_item_locations('O'):
            while not client.overloaded:
                script.strings['buff'].set('Waiting on overload')
            overload_expiry_timer = time.time() + 300
            time.sleep(5.5)
        else:
            NMZ(client, script)

        current_time = time.time()
        script.strings['health'].set(f"{client.hp} hp | {round(flick_time_threshold - current_time)} secs until pray flick.")
        script.strings['absorption'].set(f"{client.absorbs} | Drinking at {absorb_threshold}. ")


def NMZ(client, script):
    # TODO improve workflow to appear more human
    mouse = Controller()
    sleep_thresh_seed = (55, 35, 70)
    flick_time_threshold = time.time() + getTRNV(*sleep_thresh_seed)
    absorb_threshold = round(getTRNV(250, 180, 300))
    time.sleep(7)
    script.strings['status'].set('Active')
    script.post("Starting Script Now")
    while script.active:
        # print(client.current_tab != tabs.inventory)
        nmz_check(client, script)
        moved_this_loop = False
        # TODO if other scripts are run, may as well flick? human like?
        if client.hp > 1 and (rock := client.get_item_locations('(*)')):
            eatRockCake(client, script, rock)
            moved_this_loop = True
            if (flick_time_threshold - time.time()) <= 20:
                flickRapidHeal(client, script)
                flick_time_threshold = time.time() + getTRNV(*sleep_thresh_seed)

        current_time = time.time()
        script.strings['health'].set(
            f"{client.hp} hp | {round(flick_time_threshold-current_time)} secs until pray flick.")
        if time.time() >= flick_time_threshold:
            flickRapidHeal(client, script)
            flick_time_threshold = time.time() + getTRNV(*sleep_thresh_seed)
            moved_this_loop = True

        script.strings['absorption'].set(f"{client.absorbs} | Drinking at {absorb_threshold}. ")
        if client.absorbs <= absorb_threshold and (pots := client.get_item_locations('A')):
            drinkAbsorption(client, script, pots)
            absorb_threshold = round(getTRNV(250, 180, 300))
            moved_this_loop = True

        if not client.buffed and (pots := client.get_item_locations(script.style)):
            drinkBuff(client, script, pots)
            moved_this_loop = True

        x, y = mouse.position
        if client.rectangle.left < x < client.rectangle.right \
                and client.rectangle.top < y < client.rectangle.bottom and moved_this_loop:
            moveOffScreen(client, script)

        time.sleep(.2)


def nmz_check(client, script) -> None:
    if not client.inNMZ:
        timer = 1
        while timer <= 25:
            if client.inNMZ:
                script.post('NMZ Found | Resuming script')
                break
            if timer == 25:
                script.active = False
                script.post("NMZ not found. Logging out.")
                script.strings['status'].set('Program exited.')
                time.sleep(getSleepTRNV(3))
                logout(client, script)
                script.post("Logged out. ALl threads closed.")

                break
            script.post(f"{timer} / 25 Seconds until logout.")
            time.sleep(1)
            timer += 1


def drinkBuff(client, script, buffs) -> None:  # Done

    with script.lock:

        script.post("Drinking buff pot.")

        # Move to tab
        moveToTab(client, tabs.inventory)
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
        moveToTab(client, tabs.inventory)
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


def flickRapidHeal(client, script) -> None:
    with script.lock:

        # Small chance to go directly to prayer tab
        if random.randrange(1, 10) == 1:
            script.post("Moving to prayer tab to flick. (1/10 odds)")
            # Set rapid heal rect
            rect_coords = rects.rapid_heal.random_coord
            # Go to prayer tab if necessary
            moveToTab(client, tabs.prayer)
            time.sleep(getSleepTRNV(.15))
        else:
            # Set quick pray rect.
            rect_coords = rects.quick_pray.random_coord

        script.post("Flicking rapid heal now.")

        # Move to prayer location. ( Either quick pray or actual rapid heal )
        moveMouse(rect_coords)
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
        moveToTab(client, tabs.inventory)
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

    # Simply wait to look a bit more human
    time.sleep(getSleepTRNV(20))

    script.post("Logging out.")

    with script.lock:
        # Move to logout tab
        moveToTab(client, tabs.logout)
        time.sleep(getSleepTRNV(.2))

        # Move mouse to logout button
        moveMouse(rects.logout.random_coord)
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


def moveToTab(client, _tab: tab) -> None:
    # TODO: Actually implement random chance to change using f-key (Runelite needs focus)
    f_key = ''
    if client.current_tab != _tab:  # If not already on the desired tab
        rect = _tab.rect
        if random.randint(0, 1) == 100:  # Currently never returns True. Runelite needs focus for f_key to do anything.
            # Presses f key to change tabs
            pyautogui.press(f_key)
            time.sleep(getSleepTRNV(.27))
        else:  # Currently always falls to this
            # Move to tab change region
            moveMouse(rect.random_coord)
            time.sleep(getSleepTRNV(.08))

            # Clicks the tab to finish changing tabs
            pyautogui.click()
            time.sleep(getSleepTRNV(.08))


def login(client, script) -> None:  # Takes control of the mouse and keyboard to login to Runelite.
    script.post('Beginning login script.')

    # Set Runelite screenshot rect
    rect = client.rectangle
    runelite_region = (rect.left, rect.top, (rect.right - rect.left), (rect.bottom - rect.top))
    img = pyautogui.screenshot(region=runelite_region)
    current_color = img.getpixel(coords.login_box_check)

    # If on "existing user" screen, click the box to enter login page
    if pixelMatchesColor(current_color, colors.user_box_is_present, tolerance=10):
        script.post("Clicking \"Existing user\" box.")
        moveMouse(rects.existing_user.random_coord)
        time.sleep(getSleepTRNV(.4))
        pyautogui.click()
        time.sleep(getSleepTRNV(1))

    moveMouse(rects.password_input.random_coord)
    time.sleep(getSleepTRNV(.2))
    pyautogui.click()
    time.sleep(getSleepTRNV(.2))
    script.post('Typing saved password.')
    with open('assets/password.txt', 'r') as reader:
        keyboard.write(reader.readline(), .04)
    script.post('Ready to log in.')


def autoAlch(client, string_var, lock) -> None:
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
