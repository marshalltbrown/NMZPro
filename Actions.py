import keyboard
import pyautogui
import time
import random
from utilities.utils import get_random, getSleepTRNV, pixelMatchesColor
from Runelite import tabs, rects
from utilities.object_templates import tab
from utilities.vars import coords, colors


def overload(client, script):
    sleep_thresh_seed = (55, 35, 70)
    flick_time_threshold = time.time() + get_random(*sleep_thresh_seed)
    absorb_threshold = round(get_random(250, 180, 300))
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
                    absorb_threshold = round(get_random(250, 180, 300))

                if client.hp > 1 and (rock := client.get_item_locations('(*)')):
                    eatRockCake(client, script, rock)

                moveToTab(client, script, tabs.prayer)
                script.mouse.moveMouse(rects.melee_prayer.random_coord)

                while overload_expiry_timer - time.time() >= 2:
                    script.strings['buff'].set(f"Overload ends in {round(overload_expiry_timer - time.time())}")
                    time.sleep(.1)

                pyautogui.click()

                moveToTab(client, script, tabs.inventory)
                script.mouse.moveMouse(o_pot[0])
                while client.overloaded:
                    time.sleep(.0001)

                pyautogui.click()
                overload_expiry_timer = time.time() + 299

                time.sleep(getSleepTRNV(5))

                moveToTab(client, script, tabs.prayer)
                script.mouse.moveMouse(rects.melee_prayer.random_coord)
                pyautogui.click()
                flick_time_threshold = time.time() + get_random(*sleep_thresh_seed)

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
                        flick_time_threshold = time.time() + get_random(*sleep_thresh_seed)

                current_time = time.time()
                script.strings['health'].set(
                    f"{client.hp} hp | {round(flick_time_threshold - current_time)} secs until pray flick.")
                if time.time() >= flick_time_threshold:
                    flickRapidHeal(client, script)
                    flick_time_threshold = time.time() + get_random(*sleep_thresh_seed)
                    moved_this_loop = True

                script.strings['absorption'].set(f"{client.absorbs} | Drinking at {absorb_threshold}. ")
                if client.absorbs <= absorb_threshold and (pots := client.get_item_locations('A')):
                    drinkAbsorption(client, script, pots)
                    absorb_threshold = round(get_random(250, 180, 300))
                    moved_this_loop = True

                if not client.buffed and (pots := client.get_item_locations(script.style)):
                    drinkBuff(client, script, pots)
                    moved_this_loop = True

                x, y = pyautogui.position()
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
        script.strings['health'].set(
            f"{client.hp} hp | {round(flick_time_threshold - current_time)} secs until pray flick.")
        script.strings['absorption'].set(f"{client.absorbs} | Drinking at {absorb_threshold}. ")


def NMZ(client, script):
    # TODO improve workflow to appear more human
    sleep_thresh_seed = (55, 35, 70)
    flick_time_threshold = time.time() + get_random(*sleep_thresh_seed)
    absorb_threshold = round(get_random(250, 180, 300))
    time.sleep(7)
    script.strings['status'].set(f'Active | {script.style}')
    script.post("Starting Script Now")
    script.start_time = time.time()
    while script.active:
        # If the client does not have absorbs active, logout, end script, and break the loop.
        if not nmz_check(client, script):
            break
        moved_this_loop = False
        # TODO if other scripts are run, may as well flick? human like?
        if client.hp > 1 and (rock := client.get_item_locations('(*)')):
            eatRockCake(client, script, rock)
            moved_this_loop = True
            flick_time_threshold = time.time() + get_random(50, 30, 60)

        current_time = time.time()
        script.strings['health'].set(
            f"{client.hp} hp | {round(flick_time_threshold-current_time)} secs until pray flick.")
        if time.time() >= flick_time_threshold:
            flickRapidHeal(client, script)
            flick_time_threshold = time.time() + get_random(*sleep_thresh_seed)
            if client.hp > 1 and (rock := client.get_item_locations('(*)')):
                eatRockCake(client, script, rock)
            moved_this_loop = True

        script.strings['absorption'].set(f"{client.absorbs} | Drinking at {absorb_threshold}. ")
        if client.absorbs <= absorb_threshold and (pots := client.get_item_locations('A')):
            if (flick_time_threshold - time.time()) <= 30:
                flickRapidHeal(client, script)
            drinkAbsorption(client, script, pots)
            absorb_threshold = round(get_random(250, 180, 300))
            moved_this_loop = True

        if not client.buffed and (pots := client.get_item_locations(script.style)):  # TODO: Add OCR for buff pot&random
            if (flick_time_threshold - time.time()) <= 30:
                flickRapidHeal(client, script)
            drinkBuff(client, script, pots)
            moved_this_loop = True

        x, y = pyautogui.position()
        if client.rectangle.left < x < client.rectangle.right \
                and client.rectangle.top < y < client.rectangle.bottom and moved_this_loop:
            moveOffScreen(client, script)

        time.sleep(.2)


def nmz_check(client, script) -> bool:
    """Checks if the client has absorption pots active. This indicates that the player is in NMZ
    if there are no absorbs left, it returns False, Otherwise it returns True."""
    if not client.inNMZ:  # Bool set in reader class
        timer = 1
        exit_timer = 25
        while timer <= exit_timer:
            if client.inNMZ:
                script.post('NMZ Found | Resuming script')
                script.strings['status'].set(f'Active | {script.style}')
                return True
            if timer == exit_timer:
                script.active = False
                script.post("Exit timer limit reached | Logging out")
                script.strings['status'].set('Program complete')
                time.sleep(getSleepTRNV(10))
                logout(client, script)
                script.end_time = time.time()
                elapsed_time_string = time.strftime("%H:%M:%S", time.gmtime(script.end_time - script.start_time))
                script.post(f"Total runtime: {elapsed_time_string}")
                script.post("Logged out & aLl threads have been terminated.")
                return False
            if timer == 2:
                script.post('NMZ Not Found | Pausing script')
            script.strings['status'].set(f"{timer} / {exit_timer} Seconds until logout.")
            time.sleep(1)
            timer += 1
    else:
        return True


def drinkBuff(client, script, buffs) -> None:  # Done

    with script.lock:

        script.post("Drinking buff pot.")

        # Move to tab
        moveToTab(client, script, tabs.inventory)
        time.sleep(getSleepTRNV(1))

        # Move to 1st buff pot
        script.mouse.moveMouse(buffs[0])
        time.sleep(getSleepTRNV(.5))

        # Click buff pot
        pyautogui.click()
        time.sleep(getSleepTRNV(.1))

        script.post("Buff pot drank.")


def drinkAbsorption(client, script, pots) -> None:  # Done

    with script.lock:

        script.post("Drinking absorption pot.")

        # Move to tab
        moveToTab(client, script, tabs.inventory)
        time.sleep(getSleepTRNV(.3))

        # Limits pots to click to 3
        if len(pots) > 3:
            pots = pots[:3]

        # Loop to move to first 3 absorbs and drink each of them
        for i in range(len(pots)):  # Moves to absorb
            script.mouse.moveMouse(pots[i])
            time.sleep(.3)
            for _ in range(round(get_random(15, 13, 17))):  # Clicks absorb pot a pseudo random number of times.
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
            moveToTab(client, script, tabs.prayer)
            time.sleep(getSleepTRNV(.15))
        else:
            # Set quick pray rect.
            rect_coords = rects.quick_pray.random_coord

        script.post("Flicking rapid heal now.")

        # Move to prayer location. ( Either quick pray or actual rapid heal )
        script.mouse.moveMouse(rect_coords)
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
        moveToTab(client, script, tabs.inventory)
        time.sleep(getSleepTRNV(.3))

        # Move to rock cake
        script.mouse.moveMouse(rock[0])
        time.sleep(getSleepTRNV(.1))

        # Right click to bring up guzzle menu
        pyautogui.rightClick()
        time.sleep(getSleepTRNV(.2))

        # Move mouse down relative to current location to reach "Guzzle" menu option
        x, y = pyautogui.position()
        script.mouse.moveMouse((get_random(x, x - 5, x + 5), get_random(y + 41, y + 36, y + 46),))
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
        moveToTab(client, script, tabs.logout)
        time.sleep(getSleepTRNV(.2))

        # Move mouse to logout button
        script.mouse.moveMouse(rects.logout.random_coord)
        time.sleep(getSleepTRNV(.1))

        # Click logout button TODO: See if a double click is needed here
        pyautogui.click()
        time.sleep(getSleepTRNV(.1))
        pyautogui.click()
        time.sleep(getSleepTRNV(.1))


def moveOffScreen(client, script) -> None:
    with script.lock:
        # Moves the mouse just off the right side of the Runelite client
        script.mouse.moveMouse((client.rectangle.right + 10, client.rectangle.top + getSleepTRNV(300),))
        time.sleep(getSleepTRNV(.3))

        # Click off screen to be sure Runelite loses window focus
        pyautogui.click()
        time.sleep(getSleepTRNV(.2))


def moveToTab(client, script, _tab: tab) -> None:
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
            script.mouse.moveMouse(rect.random_coord)
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
        script.mouse.moveMouse(rects.existing_user.random_coord)
        time.sleep(getSleepTRNV(.4))
        pyautogui.click()
        time.sleep(getSleepTRNV(1))

    script.mouse.moveMouse(rects.password_input.random_coord)
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
    first_coords = [client.getX(.8751545117), client.getY(.3464419476)]
    second_coords = [client.getX(.8936959209), client.getY(.3164794007)]
    click_rectangle = first_coords + second_coords
    # Set Smelter
    smelter_pos = [round(client.rectangle.left + (client.client_width * .8294190358)),
                   round(client.rectangle.bottom - (client.client_height * .3689138577))]
    print(str(smelter_pos))
    smelter_color = pyautogui.pixel(smelter_pos[0], smelter_pos[1])
    print(str(smelter_pos) + " Mouse position")
    print(str(smelter_color) + " Pixel color")
    with lock:
        string_var.set("Auto-Alching")
    client.update()
    random_interval = 1
    quit_counter = 0
    pyautogui.press('f4')
    new_x = random.normalvariate(((click_rectangle[2] - click_rectangle[0]) / 2) + click_rectangle[0], 1.848448998)
    new_y = random.normalvariate(((click_rectangle[3] - click_rectangle[1]) / 2) + click_rectangle[1], 1.599684449)
    pyautogui.moveTo(new_x, new_y, 1, pyautogui.easeOutQuad)
    pyautogui.click(interval=random_interval)
    pyautogui.press('f4')
    print("Starting auto alch")
    while True:
        if keyboard.is_pressed('esc'):
            break
        if pyautogui.pixelMatchesColor(smelter_pos[0], smelter_pos[1], smelter_color, tolerance=2):
            quit_counter = 0
        elif quit_counter > 10:
            break
        if random.randrange(1, 6) == 1:
            new_x = random.normalvariate(
                ((click_rectangle[2] - click_rectangle[0]) / 2) + click_rectangle[0], 1.848448998)
            new_y = random.normalvariate(
                ((click_rectangle[3] - click_rectangle[1]) / 2) + click_rectangle[1], 1.599684449)
            print("{} , {}".format(new_x, new_y))
            pyautogui.moveTo(new_x, new_y, 1, pyautogui.easeOutQuad)
            print("Adjusting click location.")
        if random.randrange(1, 10) == 1:
            random_interval = random.uniform(0.8, 1.2)
            print("Adjusting click interval.")

        quit_counter = quit_counter + 1

        pyautogui.click(interval=random_interval)
        if pyautogui.pixelMatchesColor(smelter_pos[0], smelter_pos[1], smelter_color, tolerance=2):
            quit_counter = 0
    with lock:
        string_var.set("Auto-Alching stopped.")
