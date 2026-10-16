import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

def train_hsi(files):
    h_range = 180
    s_range = 256
    hs_matrix = np.zeros((h_range, s_range), dtype=np.int32)

    for file in files:
        image_bgr = cv2.imread(file)
        image_hsi = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV) # HSI
        row = image_hsi.shape[0]
        col = image_hsi.shape[1]
        for r in range(row):
            for c in range(col):
                h = image_hsi[r,c,0]
                s = image_hsi[r,c,1]
                hs_matrix[h, s] += 1

    return hs_matrix

def train_rgb(files):
    size = 256
    rgb_matrix = np.zeros((size, size), dtype=np.int32)

    for file in files:
        image_bgr = cv2.imread(file)
        row = image_bgr.shape[0]
        col = image_bgr.shape[1]
        for r in range(row):
            for c in range(col):
                blue, green, red = image_bgr[r, c].astype(np.float64)  # float avoids uint8 overflow
                total = blue + green + red
                if total == 0:
                    continue  # pure black has no chromaticity
                rn = int(red / total * (size - 1))
                gn = int(green / total * (size - 1))
                rgb_matrix[rn, gn] += 1

    return rgb_matrix

def normalise(matrix):
    min = np.min(matrix)
    max = np.max(matrix)
    row = matrix.shape[0]
    col = matrix.shape[1]
    normalised = np.zeros((row, col), dtype=np.float64)

    for r in range(row):
        for c in range(col):
            normalised[r, c] = (matrix[r,c] - min) / (max - min)

    return normalised

def training(files, mode):

    match mode:
        case 0:
            matrix = train_hsi(files)
        case 1:
            matrix = train_rgb(files)

    normalised_matrix = normalise(matrix)

    return normalised_matrix

def testing(file, matrix, threshold, mode):

    image_bgr = cv2.imread(file)
    image_hsi = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV) # HSI
    row = image_hsi.shape[0]
    col = image_hsi.shape[1]
    size = 256
    new_img = np.zeros_like(image_hsi)

    for r in range(row):
        for c in range(col):
            if mode == 0:
                a = image_hsi[r,c,0]
                b = image_hsi[r,c,1]
            else:
                blue, green, red = image_bgr[r, c].astype(np.float64)  # float avoids uint8 overflow
                total = blue + green + red
                if total == 0:
                    continue  # pure black has no chromaticity
                a = int(red / total * (size - 1))
                b = int(green / total * (size - 1))

            if matrix[a, b] > threshold:
                new_img[r,c] = image_bgr[r, c]

    return new_img




files = ["MP4/training/img1.jpg", "MP4/training/img2.jpg", "MP4/training/img3.jpg", "MP4/training/img4.jpg", "MP4/training/img5.jpg", "MP4/training/img6.jpg", "MP4/training/img7.jpg"]
threshold = 0.001 #HSI
#threshold = 0.0001 #RGB
mode = 0

matrix = training(files, mode)
gun1 = testing("MP4/gun1.bmp", matrix, threshold, mode)
joy1 = testing("MP4/joy1.bmp", matrix, threshold, mode)
pointer1 = testing("MP4/pointer1.bmp", matrix, threshold, mode)

cv2.imshow("gun1", gun1)
cv2.imshow("joy1", joy1)
cv2.imshow("pointer1", pointer1)

# cv2.imwrite("MP4/Results/gun_rgb.bmp", gun1)
# cv2.imwrite("MP4/Results/joy_rgb.bmp", joy1)
# cv2.imwrite("MP4/Results/pointer_rgb.bmp", pointer1)

cv2.waitKey(0)
cv2.destroyAllWindows()