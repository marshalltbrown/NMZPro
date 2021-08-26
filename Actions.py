import threading
import pyautogui
import pyperclip
import time
import random
import keyboard
import numpy as np
import matplotlib.pyplot as plt
from pynput.mouse import Button, Controller


def generateMousePlot(client):
    fig = plt.figure(figsize=[13, 13])
    plt.axis('off')
    currentx = pyautogui.position()[0]
    currenty = pyautogui.position()[1]
    destinationx = 900
    destinationy = 1000
    for y in np.linspace(currenty, destinationy, 1):
        for x in np.linspace(currentx, destinationx, 1):
            points = []
            wind_mouse(currentx, currenty, destinationx, destinationy, move_mouse=lambda x, y: points.append([x, y]))
    mouse = Controller()
    print(len(points))
    for i in points:
        mouse.move(i[0] - mouse.position[0], i[1] - mouse.position[1])
        time.sleep(1/len(points))


def wind_mouse(start_x, start_y, dest_x, dest_y, G_0=9, W_0=3, M_0=15, D_0=12, move_mouse=lambda x,y: None):
    sqrt3 = np.sqrt(3)
    sqrt5 = np.sqrt(5)
    '''
    WindMouse algorithm. Calls the move_mouse kwarg with each new step.
    Released under the terms of the GPLv3 license.
    G_0 - magnitude of the gravitational fornce
    W_0 - magnitude of the wind force fluctuations
    M_0 - maximum step size (velocity clip threshold)
    D_0 - distance where wind behavior changes from random to damped
    '''
    current_x,current_y = start_x,start_y
    v_x = v_y = W_x = W_y = 0
    while (dist:=np.hypot(dest_x-start_x,dest_y-start_y)) >= 1:
        W_mag = min(W_0, dist)
        if dist >= D_0:
            W_x = W_x/sqrt3 + (2*np.random.random()-1)*W_mag/sqrt5
            W_y = W_y/sqrt3 + (2*np.random.random()-1)*W_mag/sqrt5
        else:
            W_x /= sqrt3
            W_y /= sqrt3
            if M_0 < 3:
                M_0 = np.random.random()*3 + 3
            else:
                M_0 /= sqrt5
        v_x += W_x + G_0*(dest_x-start_x)/dist
        v_y += W_y + G_0*(dest_y-start_y)/dist
        v_mag = np.hypot(v_x, v_y)
        if v_mag > M_0:
            v_clip = M_0/2 + np.random.random()*M_0/2
            v_x = (v_x/v_mag) * v_clip
            v_y = (v_y/v_mag) * v_clip
        start_x += v_x
        start_y += v_y
        move_x = int(np.round(start_x))
        move_y = int(np.round(start_y))
        if current_x != move_x or current_y != move_y:
            #This should wait for the mouse polling interval
            move_mouse(current_x := move_x, current_y := move_y)

    return current_x, current_y



def readInventory(client, string_dict, lock_dict, inventory_table):
    tab_selected_color = [117, 40, 30]
    if pyautogui.pixelMatchesColor(client.getX(0.7849196538936959), client.getY(0.6254681647940075), tab_selected_color, tolerance=10):
        client.tab = 'Items'
        string_dict['inventory'].set('On items tab.')
    elif pyautogui.pixelMatchesColor(client.getX(0.8714462299134734), client.getY(0.6254681647940075), tab_selected_color, tolerance=10):
        client.tab = 'Prayer'
        string_dict['inventory'].set('On prayer tab.')
    else:
        client.tab = 'Unknown'
        string_dict['inventory'].set('On unknown tab.')

    one_dose = round(client.getY(.5))
    two_dose = one_dose - 7
    three_dose = two_dose - 3
    four_dose = three_dose - 2

    for y in range(7):
        starting_x = client.getX(0.7194066749072929)
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
            starting_x = starting_x + 42
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
    range_color = [35, 149, 195]
    if pyautogui.pixelMatchesColor(x, y, range_color, tolerance=40):
        return True
    else:
        return False


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
