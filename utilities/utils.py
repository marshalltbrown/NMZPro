import random
import time
from math import floor

import pyperclip
from pynput.mouse import Controller
from utilities.object_templates import rectangle
from utilities.vars import *
from utilities.windmouse import WindMouse


def getTRNV(mean: float, lower: float, upper: float) -> float:
    result = False
    while result < lower or result > upper:
        result = random.normalvariate(mean, (upper-lower) / 4)
    return result


def getSleepTRNV(mean: float or int):
    result = False
    upper = mean * 1.4
    lower = mean * .6
    while result < lower or result > upper:
        result = random.normalvariate(mean, (upper-lower) / 4)
    return result


def getTRNVCoord(rect: rectangle):

    mean_x = (rect.right + rect.left) / 2
    mean_y = (rect.top + rect.bottom) / 2
    x = getTRNV(mean_x, rect.left, rect.right)
    y = getTRNV(mean_y, rect.top, rect.bottom)
    return x, y


def moveMouse(end_coords: tuple):
    my_mouse = WindMouse(settings)
    mouse = Controller()

    start_x, start_y = mouse.position
    end_x, end_y = end_coords

    points = my_mouse.GeneratePoints(start_x, start_y, end_x, end_y)

    if len(points) <= 20:
        for i in range(len(points)):
            mouse.move(points[i][0] - mouse.position[0], points[i][1] - mouse.position[1])
            time.sleep(getSleepTRNV(.035))
    else:
        half_point = getTRNV(len(points) * .5, len(points) * .46, len(points) * .54)
        quarter_point = getTRNV(len(points) * .75, len(points) * .73, len(points) * .77)
        eight_point = getTRNV(len(points) * .925, len(points) * .915, len(points) * .935)
        fifteenth_point = getTRNV(len(points) * .9667, len(points) * .964, len(points) * .983)

        for i in range(len(points)):
            mouse.move(points[i][0] - mouse.position[0], points[i][1] - mouse.position[1])
            if i <= half_point:
                time.sleep(getSleepTRNV(.01))
            elif i <= quarter_point:
                time.sleep(getSleepTRNV(.015))
            elif i <= eight_point:
                time.sleep(getSleepTRNV(.031))
            elif i <= fifteenth_point:
                time.sleep(getSleepTRNV(.041))


def itemCheck(colors: list, sample, tolerance: int):
    counter = 0
    if pixelMatchesColor(colors[0], sample, tolerance=tolerance):
        counter += 1
    if pixelMatchesColor(colors[1], sample, tolerance=tolerance):
        counter += 1
    if pixelMatchesColor(colors[2], sample, tolerance=tolerance):
        counter += 1
    if pixelMatchesColor(colors[3], sample, tolerance=tolerance):
        counter += 1
    return counter


def readPassword() -> None:  # Reads password from the password.txt then copies it to the clipboard.
    """Copies the saved password to the clipboard."""
    with open('assets/password.txt', 'r') as reader:
        pyperclip.copy(reader.readline())
    print('Read password from file.')


def pixelMatchesColor(sampled_color, test_color, tolerance=0) -> bool:
    """Checks if sampled color is within the tolerance of the test color."""
    if type(sampled_color) == int:  # If color is an int, convert it to an RGB color tuple.
        r = sampled_color % 256
        g = floor(sampled_color / 256) % 256
        b = floor(sampled_color / (256 * 256))
        sampled_color = r, g, b

    if len(sampled_color) == 3 or len(test_color) == 3:  # RGB mode
        r, g, b = sampled_color[:3]
        exR, exG, exB = test_color[:3]
        return (abs(r - exR) <= tolerance)\
               and (abs(g - exG) <= tolerance)\
               and (abs(b - exB) <= tolerance)
    elif len(sampled_color) == 4 and len(test_color) == 4:  # RGBA mode
        r, g, b, a = sampled_color
        exR, exG, exB, exA = test_color
        return (abs(r - exR) <= tolerance)\
            and (abs(g - exG) <= tolerance)\
            and (abs(b - exB) <= tolerance)\
            and (abs(a - exA) <= tolerance)
    else:
        assert False, 'Color mode was expected to be length 3 (RGB) or 4 (RGBA), but pixel is length %s and expectedRGBColor is length %s' % (len(sampled_color), len(test_color))