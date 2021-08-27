import random
import math


class WindMouse:

    def __init__(self, settings):
        self.mouseSpeed = settings['mouseSpeed']
        self.randomSeed = math.floor(random.uniform(0.1, 1.0) * 10)
        self.randomSpeed = max((self.randomSeed / 2.0 + self.mouseSpeed) / 10.0, 0.1)

    def GeneratePoints(self, settings):
        if settings['gravity'] < 1:
            settings['gravity'] = 1
        if settings['maxStep'] == 0:
            settings['maxStep'] = 0.01

        windX = math.floor(random.uniform(0.1, 1.0) * 10)
        windY = math.floor(random.uniform(0.1, 1.0) * 10)
        velocityX = 0
        velocityY = 0

        newX = round(settings['startX'])
        newY = round(settings['startY'])

        waitDiff = settings['maxWait'] - settings['minWait']
        sqrt2 = math.sqrt(2.0)
        sqrt3 = math.sqrt(3.0)
        sqrt5 = math.sqrt(5.0)

        points = []
        currentWait = 0

        dist = self.Hypot(settings['endX'] - settings['startX'], settings['endY'] - settings['startY'])

        while dist > 1.0:
            settings['wind'] = min(settings['wind'], dist)

            if dist >= settings['targetArea']:
                w = math.floor(random.uniform(0.1, 1.0) * round(settings['wind']) * 2 + 1)

                windX = windX / sqrt3 + (w - settings['wind']) / sqrt5
                windY = windY / sqrt3 + (w - settings['wind']) / sqrt5
            else:
                windX = windX / sqrt2
                windY = windY / sqrt2
                if settings['maxStep'] < 3:
                    settings['maxStep'] = math.floor(random.uniform(0.1, 1.0) * 3) + 3.0
                else:
                    settings['maxStep'] = settings['maxStep'] / sqrt5

            velocityX += windX
            velocityY += windY
            velocityX = velocityX + (settings['gravity'] * (settings['endX'] - settings['startX'])) / dist
            velocityY = velocityY + (settings['gravity'] * (settings['endY'] - settings['startY'])) / dist

            if self.Hypot(velocityX, velocityY) > settings['maxStep']:
                randomDist = settings['maxStep'] / 2.0 + math.floor(
                    (random.uniform(0.1, 1.0) * round(settings['maxStep'])) / 2)
                veloMag = self.Hypot(velocityX, velocityY)
                velocityX = (velocityX / veloMag) * randomDist
                velocityY = (velocityY / veloMag) * randomDist

            oldX = round(settings['startX'])
            oldY = round(settings['startY'])
            settings['startX'] += velocityX
            settings['startY'] += velocityY
            dist = self.Hypot(settings['endX'] - settings['startX'], settings['endY'] - settings['startY'])
            newX = round(settings['startX'])
            newY = round(settings['startY'])

            step = self.Hypot(settings['startX'] - oldX, settings['startY'] - oldY)
            wait = round(waitDiff * (step / settings['maxStep']) + settings['minWait'])
            currentWait += wait

            if oldX != newX or oldY != newY:
                points.append([newX, newY, currentWait])

        endX = round(settings['endX'])
        endY = round(settings['endY'])

        if endX != newX or endY != newY:
            points.append([newX, newY, currentWait])

        return points

    def Hypot(self, dx, dy):
        return math.sqrt(dx * dx + dy * dy)
