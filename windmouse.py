import random
import math


class WindMouse:

    def __init__(self, settings):
        self.mouseSpeed = settings['mouseSpeed']
        self.randomSeed = math.floor(random.uniform(0.1, 1.0) * 10)
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

        windX = math.floor(random.uniform(0.1, 1.0) * 10)
        windY = math.floor(random.uniform(0.1, 1.0) * 10)
        velocityX = 0
        velocityY = 0

        newX = round(startX)
        newY = round(startY)

        waitDiff = self.maxWait - self.minWait
        sqrt2 = math.sqrt(2.0)
        sqrt3 = math.sqrt(3.0)
        sqrt5 = math.sqrt(5.0)

        points = []
        currentWait = 0

        dist = self.Hypot(endX - startX, endY - startY)

        while dist > 1.0:
            self.wind = min(self.wind, dist)

            if dist >= self.targetArea:
                w = math.floor(random.uniform(0.1, 1.0) * round(self.wind) * 2 + 1)

                windX = windX / sqrt3 + (w - self.wind) / sqrt5
                windY = windY / sqrt3 + (w - self.wind) / sqrt5
            else:
                windX = windX / sqrt2
                windY = windY / sqrt2
                if self.maxStep < 3:
                    self.maxStep = math.floor(random.uniform(0.1, 1.0) * 3) + 3.0
                else:
                    self.maxStep = self.maxStep / sqrt5

            velocityX += windX
            velocityY += windY
            velocityX = velocityX + (self.gravity * (endX - startX)) / dist
            velocityY = velocityY + (self.gravity * (endY - startY)) / dist

            if self.Hypot(velocityX, velocityY) > self.maxStep:
                randomDist = self.maxStep / 2.0 + math.floor(
                    (random.uniform(0.1, 1.0) * round(self.maxStep)) / 2)
                veloMag = self.Hypot(velocityX, velocityY)
                velocityX = (velocityX / veloMag) * randomDist
                velocityY = (velocityY / veloMag) * randomDist

            oldX = round(startX)
            oldY = round(startY)
            startX += velocityX
            startY += velocityY
            dist = self.Hypot(endX - startX, endY - startY)
            newX = round(startX)
            newY = round(startY)

            step = self.Hypot(startX - oldX, startY - oldY)
            wait = round(waitDiff * (step / self.maxStep) + self.minWait)
            currentWait += wait

            if oldX != newX or oldY != newY:
                points.append([newX, newY, currentWait])

        endX = round(endX)
        endY = round(endY)

        if endX != newX or endY != newY:
            points.append([newX, newY, currentWait])

        return points

    def Hypot(self, dx, dy):
        return math.sqrt(dx * dx + dy * dy)
