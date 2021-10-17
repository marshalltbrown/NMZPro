import random
import time
from math import floor
import pyautogui
import numpy as np
from scipy.special import comb


def get_random(mean: float, lower: float, upper: float) -> float:
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


def itemCheck(colors: list, sample, tolerance: int) -> int:
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
        ex_r, ex_g, ex_b = test_color[:3]
        return (abs(r - ex_r) <= tolerance) and (abs(g - ex_g) <= tolerance) and (abs(b - ex_b) <= tolerance)
    elif len(sampled_color) == 4 and len(test_color) == 4:  # RGBA mode
        r, g, b, a = sampled_color
        ex_r, ex_g, ex_b, ex_a = test_color
        return (abs(r - ex_r) <= tolerance)\
            and (abs(g - ex_g) <= tolerance)\
            and (abs(b - ex_b) <= tolerance)\
            and (abs(a - ex_a) <= tolerance)
    else:
        assert False, 'Color mode was expected to be length 3 (RGB) or 4 (RGBA),' \
                      ' but pixel is length %s and expectedRGBColor is length %s'\
                      % (len(sampled_color), len(test_color))


class WindMouse:
    sqrt3 = np.sqrt(3)
    sqrt5 = np.sqrt(5)

    def __init__(self, settings):
        self.gravity = settings['gravity']
        self.wind = settings['wind']
        self.max_step = settings['maxStep']
        self.target_distance = settings['targetArea']

    @staticmethod
    def bernstein_poly(i, n, t):
        """
         The Bernstein polynomial of n, i as a function of t
        """

        return comb(n, i) * (t ** (n - i)) * (1 - t) ** i

    def moveMouse(self, end_coords: tuple) -> None:

        pyautogui.MINIMUM_DURATION = 0
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0
        movement_path = []
        self.GeneratePoints(pyautogui.position(), end_coords, move_mouse=lambda x, y: movement_path.append([x, y]))
        print(f"Number of point in path: {len(movement_path)}")
        movement_delays = WindMouse.generate_mouse_movement_sleep_array(len(movement_path))

        for i in range(len(movement_path)):
            new_x, new_y = movement_path[i]
            pyautogui.moveTo(new_x, new_y)
            time.sleep(movement_delays[i])

    @staticmethod
    def generate_mouse_movement_sleep_array(number_of_points: int) -> [float]:
        curve_points = [.01, .01, .03]  # This defines the curve distribution of the array
        t = np.linspace(0.0, 1.0, number_of_points)
        polynomial_array = np.array(
            [WindMouse.bernstein_poly(i, len(curve_points) - 1, t) for i in range(0, len(curve_points))])
        sleep_array = reversed(np.dot(np.array(curve_points), polynomial_array))
        sleep_array = [float(i) for i in sleep_array]
        return sleep_array

    def GeneratePoints(self, starting_point, destination_point, move_mouse=lambda x, y: None):
        """
        WindMouse algorithm. Calls the move_mouse kwarg with each new step.
        Released under the terms of the GPLv3 license.
        G_0 - magnitude of the gravitational force
        W_0 - magnitude of the wind force fluctuations
        M_0 - maximum step size (velocity clip threshold)
        D_0 - distance where wind behavior changes from random to damped
        """
        start_x, start_y = starting_point
        current_x, current_y = start_x, start_y
        destination_x, destination_y = destination_point
        v_x = v_y = w_x = w_y = 0
        while (dist := np.hypot(destination_x - start_x, destination_y - start_y)) >= 1:
            w_mag = min(self.wind, dist)
            if dist >= self.target_distance:
                w_x = w_x / self.sqrt3 + (2 * np.random.random() - 1) * w_mag / self.sqrt5
                w_y = w_y / self.sqrt3 + (2 * np.random.random() - 1) * w_mag / self.sqrt5
            else:
                w_x /= self.sqrt3
                w_y /= self.sqrt3
                if self.max_step < 3:
                    self.max_step = np.random.random() * 3 + 3
                else:
                    self.max_step /= self.sqrt5
            v_x += w_x + self.gravity * (destination_x - start_x) / dist
            v_y += w_y + self.gravity * (destination_y - start_y) / dist
            v_mag = np.hypot(v_x, v_y)
            if v_mag > self.max_step:
                v_clip = self.max_step / 2 + np.random.random() * self.max_step / 2
                v_x = (v_x / v_mag) * v_clip
                v_y = (v_y / v_mag) * v_clip
            start_x += v_x
            start_y += v_y
            move_x = int(np.round(start_x))
            move_y = int(np.round(start_y))
            if current_x != move_x or current_y != move_y:
                # This should wait for the mouse polling interval
                move_mouse(current_x := move_x, current_y := move_y)
        return current_x, current_y
