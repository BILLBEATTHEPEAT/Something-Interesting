# This code is written by haojian in https://gist.github.com/haojian/0ee6dd444994fd67f63b.
# Copied the code and do some modification to generate beautiful picture from the book Secret Garden.
# 2017. 9. 1

import skimage; 
from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, square
from skimage.measure import regionprops
from skimage.color import label2rgb
import cv2
import numpy as np



if __name__ == '__main__':
	print(skimage.__version__)

	origin_pic = 'pic2.jpg'

	img = data.imread(origin_pic, 1)

	print type(img), img.shape, type(img[0][0])
	thresh = threshold_otsu(img)
	bw = closing(img > thresh, square(1))
	cleared = bw.copy()
	clear_border(cleared)
	
	# label image regions
	label_image = label(cleared)
	borders = np.logical_xor(bw, cleared)
	label_image[borders] = -1
	colors = np.random.rand(500, 100);
	background = np.random.rand(3);
	image_label_overlay = label2rgb(label_image, image=img, colors=colors, bg_color=background)
	cv2.imwrite('Done.png',image_label_overlay*255)
