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


def Lighting(img):

    rows = img.shape[0]
    columns = img.shape[1]

    A = np.zeros((rows**2,3))
    x = np.zeros((3,1))
    t = img.reshape(-1,1)

    k = 0
    for r in range(256):
        for c in range(256):
            A[k] = (r+1,c+1,1)
            k += 1

    At = np.transpose(A)
    x = ((np.linalg.inv(At @ A)) @ At) @ t

    lighting = A @ x
    avg = np.mean(lighting)
    lighting = lighting.reshape(256,256)
    img_new = (img - lighting) + avg

    for r in range(256):
        for c in range(256):
            if img_new[r][c] < 0:
                img_new[r][c] = 0
            elif img_new[r][c] > 255:
                img_new[r][c] = 255

    return img_new


def HistoEqualization(img_in):

    img, img_new = read_img(img_in)
    h = histogram(img)

    rows = img.shape[0]
    columns = img.shape[1]
    for r in range(rows):
        for c in range(columns): 
            Intensity = img[r][c]
            img_new[r][c] = 255 * h[Intensity]


    img_light = Lighting(img_new)  
 
    return img_new, img_light


moon, moon_light = HistoEqualization("MP3/moon.bmp")
cv2.imshow("Moon", moon.astype(np.uint8))
cv2.imshow("Moon_light", moon_light.astype(np.uint8))

cv2.waitKey(0)
cv2.destroyAllWindows()