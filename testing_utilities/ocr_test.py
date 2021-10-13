import cv2
from easyocr import Reader
import win32ui
from PIL import Image
import pyautogui
import time
import numpy as np


from matplotlib import pyplot as plt, cm, colors


def show_image(image):
	imageio = Image.fromarray(image)
	imageio.show()


def resize_image(image):
	basewidth = 75
	wpercent = (basewidth / float(image.size[0]))
	hsize = int((float(image.size[1]) * float(wpercent)))
	img = image.resize((basewidth, hsize), Image.ANTIALIAS)
	return img


def screenshot(my_region, resize=True):
	if my_region:
		img = pyautogui.screenshot(region=my_region)
	else:
		img = pyautogui.screenshot()
	if resize:
		img = resize_image(img)
	return np.array(img)


def read(ocr, img, path=False, whitelist='0123456789'):
	if path:
		image = Image.open(img)
	else:
		image = img

	word = ocr.readtext(image, allowlist=whitelist, detail=0)

	return word


def rgb_chart(img):
	r, g, b = cv2.split(img)
	fig = plt.figure()
	axis = fig.add_subplot(1, 1, 1, projection="3d")
	pixel_colors = img.reshape((np.shape(img)[0] * np.shape(img)[1], 3))
	norm = colors.Normalize(vmin=-1., vmax=1.)
	norm.autoscale(pixel_colors)
	pixel_colors = norm(pixel_colors).tolist()
	axis.scatter(r.flatten(), g.flatten(), b.flatten(), facecolors=pixel_colors, marker=".")
	axis.set_xlabel("Red")
	axis.set_ylabel("Green")
	axis.set_zlabel("Blue")
	plt.show()


def hsv_chart(hsv):
	h, s, v = cv2.split(hsv)
	fig = plt.figure()
	axis = fig.add_subplot(1, 1, 1, projection="3d")
	pixel_colors = hsv.reshape((np.shape(hsv)[0] * np.shape(hsv)[1], 3))
	norm = colors.Normalize(vmin=-1., vmax=1.)
	norm.autoscale(pixel_colors)
	pixel_colors = norm(pixel_colors).tolist()
	axis.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker=".")
	axis.set_xlabel("Hue")
	axis.set_ylabel("Saturation")
	axis.set_zlabel("Value")
	plt.show()


def show_threshs(low, high):
	lo_square = np.full((10, 10, 3), low, dtype=np.uint8) / 255.0
	do_square = np.full((10, 10, 3), high, dtype=np.uint8) / 255.0
	plt.subplot(1, 2, 1)
	plt.imshow(colors.hsv_to_rgb(do_square))
	plt.subplot(1, 2, 2)
	plt.imshow(colors.hsv_to_rgb(lo_square))
	plt.show()


def filter_hp(img):
	low_thresh = (60, 160, 160)
	high_thresh = (255, 260, 260)
	hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv_img, low_thresh, high_thresh)
	blur = cv2.GaussianBlur(mask, (7, 7), 0)
	return blur


def run():

	window = win32ui.FindWindow(None, "RuneLite")
	l, t, r, b = window.GetWindowRect()
	runelite_region = (l, t, r-l, b-t,)
	# Health bar screenshot
	left = 27 + l
	top = 95 + t
	width = 29
	height = 12
	hp_region = (left, top, width, height,)

	ocr = Reader(['en'], gpu=True)
	for i in range(1):
		img = screenshot(my_region=hp_region)
		#img = cv2.imread('img/376.png')
		post_img = filter_hp(img)
		# hsv_chart(post_img)
		# result = cv2.bitwise_and(img, img, mask=mask)

		print(f"Raw: {read(ocr, img)} Edited: {read(ocr, post_img)}")
		time.sleep(1)

		plt.subplot(1, 2, 1)
		plt.imshow(img)
		plt.subplot(1, 2, 2)
		plt.imshow(post_img)
		plt.show()

if __name__ == '__main__':
	run()

