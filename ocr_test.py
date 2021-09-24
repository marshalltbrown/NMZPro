import cv2
from easyocr import Reader
import win32ui
from PIL import Image
import pyautogui
import time
import numpy as np
import os


def show_image(image):
	imageio = Image.fromarray(image)
	imageio.show()


def resize_image(image):
	basewidth = 100
	wpercent = (basewidth / float(image.size[0]))
	hsize = int((float(image.size[1]) * float(wpercent)))
	img = image.resize((basewidth, hsize), Image.ANTIALIAS)
	return img


def cleanup_text(text):
	# strip out non-ASCII text so we can draw the text on the image
	# using OpenCV
	return "".join([c if ord(c) < 128 else "" for c in text]).strip()


window = win32ui.FindWindow(None, "RuneLite")
l, t, r, b = window.GetWindowRect()

# Health bar screenshot
left = 524 + l
top = 82 + t
width = 545 - 524
height = 95 - 82


ocr = Reader(['en'], gpu=True)

timer = time.time()
counter = 0
iters = 1
for i in range(iters):
	img = pyautogui.screenshot(region=(left, top, width, height,))
	img = np.array(resize_image(img))
	## convert to hsv
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	## mask of green (36,25,25) ~ (86, 255,255)
	# mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
	mask = cv2.inRange(hsv, (36, 25, 25), (70, 255, 255))

	## slice the green
	imask = mask > 0
	green = np.zeros_like(img, np.uint8)
	green[imask] = img[imask]

	cv2.imwrite(img, green)

	show_image(img)
	word = ocr.readtext(img, allowlist='0123456789', detail=0)
	time_dif = time.time() - timer
	print(f"Word: {word}, Time: {time_dif}")

	counter += time_dif
	timer = time.time()

print(f"Average OCR time: {counter/iters}")

#
#

