import random

import pyperclip
import re
import win32ui
from vars import *
from windmouse import WindMouse
from pynput.mouse import Controller
import time
from math import floor
from scipy.stats import truncnorm


def getTRNV(mean, lower, upper):
    result = False
    while result < lower or result > upper:
        result = random.normalvariate(mean, (upper-lower) / 4)
    return result


def getTRNVCoord(rect):
    mean_x = (rect.right + rect.left) / 2
    mean_y = (rect.top + rect.bottom) / 2
    x = getTRNV(mean_x, rect.lower, rect.right)
    y = getTRNV(mean_y, rect.top, rect.bottom)
    return x, y


def getTruncatedNormal(mean=0, sd=1, low=0, upp=10):
    return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd).rvs()


def generateMousePlot(end_coords):
    myMouse = WindMouse(settings)
    mouse = Controller()
    endX, endY = end_coords
    startX, startY = mouse.position

    points = myMouse.GeneratePoints(startX, startY, endX, endY)

    #Move the mouse across the points

    for i in range(len(points)):
        mouse.move(points[i][0] - mouse.position[0], points[i][1] - mouse.position[1])
        time.sleep(1/len(points))


def decimalColortoRGB(decimal):
    r = decimal % 256
    g = floor(decimal / 256) % 256
    b = floor(decimal / (256 * 256))
    return r, g, b


def getColor(coords):
    x, y = coords
    window_title = re.compile
    try:
        window = win32ui.FindWindow(None, "Runelite - BigMTB")
    except:
        window = win32ui.FindWindow(None, "Runelite")
    dc = window.GetWindowDC()
    color = 1, 1, 1
    try:
        color = dc.GetPixel(x, y)
    except:
        print("Error in inventory thread.")
    dc.DeleteDC()
    return color


def readPassword():  # Reads password from the password.txt then copies it to the clipboard.
    with open('password.txt', 'r') as reader:
        pyperclip.copy(reader.readline())
    print('Read password from file.')


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