#!/usr/bin/env python3

import cv2
import numpy as np
from matplotlib import pyplot as plt

def plot(img, edges):
	# f = plt.figure()
	# f.add_subplot(1, 2, 1)
	# plt.imshow(np.rot90(img, 2))
	# f.add_subplot(1, 2, 2)
	# plt.imshow(np.rot90(edges, 2))
	# plt.show(block=True)

	plt.subplot(121)
	plt.imshow(img, cmap = 'gray')
	plt.title('Original Image')
	plt.xticks([])
	plt.yticks([])
	plt.subplot(122)
	plt.imshow(edges, cmap = 'gray')
	plt.title('Edge Image')
	plt.xticks([])
	plt.yticks([])
	plt.show()


img = cv2.imread("/home/asif/Downloads/ibas/ibas-faq/faq-01.png")

# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Performing OTSU threshold
# ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

edges = cv2.Canny(gray, 20, 20)
plot(gray, edges)



