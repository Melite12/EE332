import cv2
import numpy as np
import math

def read_img(filename):

    img = cv2.imread(filename) 
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    gray_img_new = np.zeros_like(gray_img)

    return gray_img, gray_img_new

def histogram(img):

    h = np.zeros(256)
    rows = img.shape[0]
    columns = img.shape[1]
    for r in range(rows):
        for c in range(columns): 
            Intensity = img[r][c]
            h[Intensity] += 1

    total_pixels = rows * columns
    sum = 0
    for idx, val in enumerate(h):
        sum += val
        h[idx] = sum / total_pixels

    return h

def HistoEqualization(img_in):

    img, img_new = read_img(img_in)
    h = histogram(img)

    rows = img.shape[0]
    columns = img.shape[1]
    for r in range(rows):
        for c in range(columns): 
            Intensity = img[r][c]
            img_new[r][c] = 255 * h[Intensity]

    return img_new




moon = HistoEqualization("MP3/moon.bmp")
cv2.imshow("Moon", moon)

cv2.waitKey(0)
cv2.destroyAllWindows()