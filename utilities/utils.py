import random
import time
from math import floor, sqrt

from pynput.mouse import Controller
from utilities.vars import settings


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


def Hypot(dx, dy):
    return sqrt(dx * dx + dy * dy)


class WindMouse:

    def __init__(self, settings):
        self.mouseSpeed = settings['mouseSpeed']
        self.randomSeed = floor(random.uniform(0.1, 1.0) * 10)
        self.randomSpeed = max((self.randomSeed / 2.0 + self.mouseSpeed) / 10.0, 0.1)
        self.gravity = settings['gravity']
        self.wind = settings['wind']
        self.maxStep = settings['maxStep']
        self.minWait = settings['minWait']
        self.maxWait = settings['maxWait']
        self.targetArea = settings['targetArea']
        self.maxWait = settings['maxWait']

    def processVariables(self):
        if self.gravity < 1:
            self.gravity = 1
        if self.maxStep == 0:
            self.maxStep = 0.01

    def GeneratePoints(self, startX, startY, endX, endY):

        windX = floor(random.uniform(0.1, 1.0) * 10)
        windY = floor(random.uniform(0.1, 1.0) * 10)
        velocityX = 0
        velocityY = 0

        newX = round(startX)
        newY = round(startY)

        waitDiff = self.maxWait - self.minWait
        sqrt2 = sqrt(2.0)
        sqrt3 = sqrt(3.0)
        sqrt5 = sqrt(5.0)

        points = []
        currentWait = 0

        dist = Hypot(endX - startX, endY - startY)

        while dist > 1.0:
            self.wind = min(self.wind, dist)

            if dist >= self.targetArea:
                w = floor(random.uniform(0.1, 1.0) * round(self.wind) * 2 + 1)

                windX = windX / sqrt3 + (w - self.wind) / sqrt5
                windY = windY / sqrt3 + (w - self.wind) / sqrt5
            else:
                windX = windX / sqrt2
                windY = windY / sqrt2
                if self.maxStep < 3:
                    self.maxStep = floor(random.uniform(0.1, 1.0) * 3) + 3.0
                else:
                    self.maxStep = self.maxStep / sqrt5

            velocityX += windX
            velocityY += windY
            velocityX = velocityX + (self.gravity * (endX - startX)) / dist
            velocityY = velocityY + (self.gravity * (endY - startY)) / dist

            if Hypot(velocityX, velocityY) > self.maxStep:
                randomDist = self.maxStep / 2.0 + floor(
                    (random.uniform(0.1, 1.0) * round(self.maxStep)) / 2)
                veloMag = Hypot(velocityX, velocityY)
                velocityX = (velocityX / veloMag) * randomDist
                velocityY = (velocityY / veloMag) * randomDist

            oldX = round(startX)
            oldY = round(startY)
            startX += velocityX
            startY += velocityY
            dist = Hypot(endX - startX, endY - startY)
            newX = round(startX)
            newY = round(startY)

            step = Hypot(startX - oldX, startY - oldY)
            wait = round(waitDiff * (step / self.maxStep) + self.minWait)
            currentWait += wait

            if oldX != newX or oldY != newY:
                points.append([newX, newY, currentWait])

        endX = round(endX)
        endY = round(endY)

        if endX != newX or endY != newY:
            points.append([newX, newY, currentWait])

        return points
