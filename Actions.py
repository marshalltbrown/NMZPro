import threading
from math import floor
import pyautogui
import pyperclip
import time
import random
import keyboard
import win32ui
from vars import *
from windmouse import WindMouse
from pynput.mouse import Controller


def win32test(coords):
    print(coords)
    x, y = coords
    window = win32ui.FindWindow(None, "Runelite - BigMTB")
    dc = window.GetWindowDC()
    color = dc.GetPixel(x, y)
    dc.DeleteDC()
    return color

def generateMousePlot(end_coords):
    myMouse = WindMouse(settings)
    mouse = Controller()
    endX, endY = end_coords
    startX, startY = pyautogui.position()

    points = myMouse.GeneratePoints(startX, startY, endX, endY)

    #Move the mouse across the points

    for i in range(len(points)):
        mouse.move(points[i][0] - mouse.position[0], points[i][1] - mouse.position[1])
        time.sleep(1/len(points))


def readInventory(client, string_dict, lock_dict, inventory_table):
    current_color = win32test(coord_item_tab_check)
    current_color2 = win32test(coord_prayer_tab_check)
    if pixelMatchesColor(current_color, color_tab_selected, tolerance=10):
        client.tab = 'Items'
        string_dict['inventory'].set('On items tab.')

    elif pixelMatchesColor(current_color2, color_tab_selected, tolerance=10):
        client.tab = 'Prayer'
        string_dict['inventory'].set('On prayer tab.')
    else:
        client.tab = 'Unknown'
        string_dict['inventory'].set('On unknown tab.')

    one_dose = coord_inv_slot1_1[1]
    two_dose = one_dose - 7
    three_dose = two_dose - 3
    four_dose = three_dose - 2
    starting_x = coord_inv_slot1_1[0]
    print(f"x: {starting_x}, Y: {one_dose}")
    for y in range(7):
        starting_x = starting_x + 42
        for x in range(4):
            if getColors(starting_x, four_dose):
                inventory_table[x][y].set('4')
            elif getColors(starting_x, three_dose):
                inventory_table[x][y].set('3')
            elif getColors(starting_x, two_dose):
                inventory_table[x][y].set('2')
            elif getColors(starting_x, one_dose):
                inventory_table[x][y].set('1')
            else:
                inventory_table[x][y].set('  -  ')

        four_dose += 36
        three_dose += 36
        two_dose += 36
        one_dose += 36


def readHealth(client):
    health_color = [255, 6, 0]
    if pyautogui.pixelMatchesColor(client.getX(0.6613102595797281), client.getY(0.8408239700374532), health_color, tolerance=10)\
            and pyautogui.pixelMatchesColor(client.getX(0.6613102595797281), client.getY(0.8277153558052435), health_color, tolerance=10)\
            and not pyautogui.pixelMatchesColor(client.getX(0.6588380716934487), client.getY(0.8389513108614233), health_color, tolerance=10):
        client.health = '1'
        return '1 hp'
    else:
        client.health = 'Unknown'
        return '? hp'


def getColors(x, y):
    #print(f"--------Color at click: {str(pyautogui.pixel(X, Y))}")
    var = x, y
    current_color = win32test(var)
    if pixelMatchesColor(current_color, color_range_potion, tolerance=40):
        return True
    else:
        return False


def expandToWin(client, coords):
    x, y = coords
    x += client.client_rectangle.left
    y += client.client_rectangle.top
    return x, y



def NMZmoveToRapidHeal(x, y):
    pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)


def NMZ(client, status_var, health_var, lock, health_lock):
    client.setFocus()
    status_var.set('NMZ Started.')
    newx = random.normalvariate(((client.getX(0.9060568603213844) - client.getX(0.8726823238566132)) / 2) + client.getX(0.8726823238566132), 5.247710123)
    newy = random.normalvariate(((client.getY(0.4250936329588015) - client.getY(0.4737827715355805)) / 2) + client.getY(0.4737827715355805), 4.446260313)
    with lock:
        if client.tab != 'prayer':
            pyautogui.press('f3')
        NMZmoveToRapidHeal(newx, newy)
    while True:
        if client.health != '1' and client.eating == 'Pending':
            client.eating = 'Eating'
            newx = random.normalvariate(((client.getX(0.9060568603213844) - client.getX(0.8726823238566132)) / 2) + client.getX(0.8726823238566132), 5.247710123)
            newy = random.normalvariate(((client.getY(0.4250936329588015) - client.getY(0.4737827715355805)) / 2) + client.getY(0.4737827715355805), 4.446260313)
            threading.Thread(target=eatRockCake, args=(client, health_var, lock, health_lock,), daemon=True).start()
        with lock:
            client.setFocus()
            status_var.set("Flicking Rapid Heal now.")
            NMZmoveToRapidHeal(newx, newy)
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
                NMZmoveToRapidHeal(newx, newy)
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


def readPassword():  # Reads password from the password.txt then copies it to the clipboard.
    with open('password.txt', 'r') as reader:
        pyperclip.copy(reader.readline())
    print('Read password from file.')


def login(client):  # Takes control of the mouse and keyboard to login to Runelite.
    print('Beginning login script.')
    client.updateClient()
    client.setFocus()
    current_color = win32test(coord_login_box_check)
    if pixelMatchesColor(current_color, color_user_box_is_present, tolerance=10):
        print("Clicking \"Existing user\" box.")
        generateMousePlot(expandToWin(client, coord_login_box_check))
        pyautogui.click()
        time.sleep(random.normalvariate(.5, .1))
    generateMousePlot(expandToWin(client, coord_login_entry))
    pyautogui.click()
    pyautogui.keyDown('ctrl')
    pyautogui.press('v')
    pyautogui.keyUp('ctrl')
    print('Logged in.')


def decimalColortoRGB(decimal):
    r = floor(decimal / (256 * 256))
    g = floor(decimal / 256) % 256
    b = decimal % 256
    return r, g, b


def pixelMatchesColor(pix, expectedRGBColor, tolerance=0):
    if type(pix) == int:
        pix = decimalColortoRGB(pix)
    if len(pix) == 3 or len(expectedRGBColor) == 3: #RGB mode
        r, g, b = pix[:3]
        exR, exG, exB = expectedRGBColor[:3]
        return (abs(r - exR) <= tolerance) and (abs(g - exG) <= tolerance) and (abs(b - exB) <= tolerance)
    elif len(pix) == 4 and len(expectedRGBColor) == 4: #RGBA mode
        r, g, b, a = pix
        exR, exG, exB, exA = expectedRGBColor
        return (abs(r - exR) <= tolerance) and (abs(g - exG) <= tolerance) and (abs(b - exB) <= tolerance) and (abs(a - exA) <= tolerance)
    else:
        assert False, 'Color mode was expected to be length 3 (RGB) or 4 (RGBA), but pixel is length %s and expectedRGBColor is length %s' % (len(pix), len(expectedRGBColor))


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
    smelterPOS = [round(client.client_rectangle.left + (client.client_width * .8294190358)),
                  round(client.client_rectangle.bottom - (client.client_height * .3689138577))]
    print(str(smelterPOS))
    smelterColor = pyautogui.pixel(smelterPOS[0], smelterPOS[1])
    print(str(smelterPOS) + " Mouse position")
    print(str(smelterColor) + " Pixel color")
    with lock:
        string_var.set("Auto-Alching")
    client.updateClient()
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
