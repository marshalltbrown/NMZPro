import math

import pyautogui
import pyperclip
import time
import random
import keyboard


def readInventory(client, gamestate):
    tab_selected_color = [117, 40, 30]
    if pyautogui.pixelMatchesColor(client.getX(0.7849196538936959), client.getY(0.6254681647940075), tab_selected_color, tolerance=10):
        gamestate['tab'] = 'items'
        return 'On items tab.'
    elif pyautogui.pixelMatchesColor(client.getX(0.8714462299134734), client.getY(0.6254681647940075), tab_selected_color, tolerance=10):
        gamestate['tab'] = 'prayer'
        return 'On prayer tab.'
    else:
        gamestate['tab'] = 'unknown'
        return 'On unknown tab.'


def readHealth(client, gamestate):
    health_color = [255, 6, 0]
    if pyautogui.pixelMatchesColor(client.getX(0.6613102595797281), client.getY(0.8408239700374532), health_color, tolerance=10)\
            and pyautogui.pixelMatchesColor(client.getX(0.6613102595797281), client.getY(0.8277153558052435), health_color, tolerance=10)\
            and not pyautogui.pixelMatchesColor(client.getX(0.6588380716934487), client.getY(0.8389513108614233), health_color, tolerance=10):
        gamestate['health'] = '1'
        return '1 hp'
    else:
        gamestate['health'] = 'Unknown'
        return '? hp'


def NMZmoveToRapidHeal(x, y):
    pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)


def NMZ(client, gamestate, string_var):
    client.setFocus()
    string_var.set('NMZ Started.')
    newx = random.normalvariate(((client.getX(0.9060568603213844) - client.getX(0.8726823238566132)) / 2) + client.getX(0.8726823238566132), 5.247710123)
    newy = random.normalvariate(((client.getY(0.4250936329588015) - client.getY(0.4737827715355805)) / 2) + client.getY(0.4737827715355805), 4.446260313)
    if gamestate['tab'] != 'prayer':
        pyautogui.press('f3')
    NMZmoveToRapidHeal(newx, newy)
    while True:
        pyautogui.click()
        time.sleep(random.normalvariate(.5, .15))
        pyautogui.click()
        sleep_duration = round(random.normalvariate(50, 5))
        if random.randrange(1, 6) == 1:
            newx = random.normalvariate(((client.getX(0.9060568603213844) - client.getX(0.8726823238566132)) / 2) + client.getX(0.8726823238566132), 5.247710123)
            newy = random.normalvariate(((client.getY(0.4250936329588015) - client.getY(0.4737827715355805)) / 2) + client.getY(0.4737827715355805), 4.446260313)
            NMZmoveToRapidHeal(newx, newy)
        for timer in range(sleep_duration):
            string_var.set(f"Waiting {timer}/{sleep_duration} seconds.")
            time.sleep(1)


def readPassword():  # Reads password from the password.txt then copies it to the clipboard.
    with open('password.txt', 'r') as reader:
        pyperclip.copy(reader.readline())
    print('Read password from file.')


def login(client):  # Takes control of the mouse and keyboard to login to Runelite.
    print('Beginning login script.')
    client.updateClient()
    client.setFocus()
    existing_user_box_on_screen = [19, 20, 21]
    if pyautogui.pixelMatchesColor(client.getX(0.48825710754017304), client.getY(0.4101123595505618), existing_user_box_on_screen, tolerance=10):
        print("Clicking \"Existing user\" box.")
        pyautogui.click(client.getX(0.48825710754017304), client.getY(0.4101123595505618), interval=1)
    pyautogui.click(client.getX(.4326328801), client.getY(.4588014981), interval=1)
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
        if (random.randrange(1, 6) == 1):
            newx = random.normalvariate(((clickrectangle[2] - clickrectangle[0]) / 2) + clickrectangle[0], 1.848448998)
            newy = random.normalvariate(((clickrectangle[3] - clickrectangle[1]) / 2) + clickrectangle[1], 1.599684449)
            print("{} , {}".format(newx, newy))
            # pyautogui.moveTo(random.randrange(clickrectangle[0], clickrectangle[2]),random.randrange(clickrectangle[1], clickrectangle[3]), 1, pyautogui.easeOutQuad)
            pyautogui.moveTo(newx, newy, 1, pyautogui.easeOutQuad)
            print("Adjusting click location.")
        if (random.randrange(1, 10) == 1):
            randominterval = random.uniform(0.8, 1.2)
            print("Adjusting click interval.")

        quitCounter = quitCounter + 1

        pyautogui.click(interval=randominterval)
        if pyautogui.pixelMatchesColor(smelterPOS[0], smelterPOS[1], smelterColor, tolerance=2):
            quitCounter = 0
    with lock:
        string_var.set("Auto-Alching stopped.")
