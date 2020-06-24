import cv2
import numpy as np
from skimage import io
import matplotlib.pyplot as plt


img = io.imread('/bighdd/projects/PHP/parsing-houzz/downloaded-images/0b7a1e67cb194309269f5bd6cd11fec2.jpg')[:, :, :-1]




average = img.mean(axis=0).mean(axis=0)

pixels = np.float32(img.reshape(-1, 3))

n_colors = 5
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
flags = cv2.KMEANS_RANDOM_CENTERS

_, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
_, counts = np.unique(labels, return_counts=True)

dominant = palette[np.argmax(counts)]



print(palette)