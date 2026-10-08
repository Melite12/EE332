import cv2
import numpy as np
import math

def read_img(filename):
    img = cv2.imread(filename, 0) 
    img = (img != 0).astype(np.uint8) # make img array into 1's and 0's instead of 255 and 0s
    img_new = (np.zeros((img.shape[0],img.shape[1]))).astype(np.uint8)

    return img, img_new

def apply_SE(img, SE, r, c, code):
    for r_idx, r_new in enumerate(range(r, r + SE.shape[0])):
        for c_idx, c_new in enumerate(range (c, c + SE.shape[1])):
            if r_new < 0 or c_new < 0 :
                continue

            if r_new >= img.shape[0] or c_new >= img.shape[1]:
                continue

            match code:
                case 0:
                    if SE[r_idx][c_idx] * img[r_new][c_new] == 1:
                        return True
                case 1:
                    if SE[r_idx][c_idx] == 1 and img[r_new][c_new] == 0:
                        return True
    return False

def Erosion(filename, SE):

    img, img_erosion = read_img(filename)
    row_center = math.floor(SE.shape[0] / 2) # The row of the center
    col_center = math.floor(SE.shape[1] / 2) # The column of the center

    for r in range(img.shape[0]):
        for c in range(img.shape[1]):
            if img[r][c] == 1:
                val = apply_SE(img, SE, r-row_center ,c-col_center, 1)
                img_erosion[r][c] = 1 if val else 0

    img_erosion = img - img_erosion
    return img_erosion

def Dilation(filename, SE):

    img, img_dilation = read_img(filename)
    row_center = math.floor(SE.shape[0] / 2) # The column of the center
    col_center = math.floor(SE.shape[1] / 2) # The row of the center

    for r in range(img.shape[0]):
        for c in range(img.shape[1]):
            if img[r][c] == 0:
                val = apply_SE(img, SE, r-row_center ,c-col_center, 0)
                img_dilation[r][c] = 1 if val else 0
    
    img_dilation = img_dilation | img
    return img_dilation


def Opening(filename, SE):

    img_erosion = Erosion(filename, SE)
    cv2.imwrite("MP2/Results/erosion.bmp", img_erosion)
    img_opening = Dilation("MP2/Results/erosion.bmp", SE)

    return img_opening

def Closing(filename, SE):

    img_dilation = Dilation(filename, SE)
    cv2.imwrite("MP2/Results/dilation.bmp", img_dilation)
    img_closing = Erosion("MP2/Results/dilation.bmp", SE)

    return img_closing

def Boundary(filename, SE):
    
    img_erosion = Erosion(filename, SE)
    img, img_boundary = read_img(filename)
    img_boundary = img - img_erosion

    return img_boundary



SE1 = np.array([[1,1,1],
                [1,1,1],
                [1,1,1],])

SE2 = np.array([[0,1,0],
                [1,1,1],
                [0,1,0],])

SE3 = np.array([[1,1,1,1,1],
                [1,1,1,1,1],
                [1,1,1,1,1],
                [1,1,1,1,1],
                [1,1,1,1,1]])

SE4 = np.array([[1,1,1,1],
                [1,1,1,1],
                [1,1,1,1],
                [1,1,1,1],])

SE = SE1

gun_erosion = Erosion("MP2/gun.bmp", SE) * 250
gun_dilation = Dilation("MP2/gun.bmp", SE) * 250
gun_opening = Opening("MP2/gun.bmp", SE) * 250
gun_closing = Closing("MP2/gun.bmp", SE) * 250
gun_boundary = Boundary("MP2/gun.bmp", SE) * 250

# cv2.imshow("Gun_E", gun_erosion)
# cv2.imshow("Gun_D", gun_dilation)
# cv2.imshow("Gun_O", gun_opening)
cv2.imshow("Gun_C", gun_closing)
cv2.imshow("Gun_B", gun_boundary)

Palm_erosion = Erosion("MP2/Palm.bmp", SE) * 250
Palm_dilation = Dilation("MP2/Palm.bmp", SE) * 250
Palm_opening = Opening("MP2/Palm.bmp", SE) * 250
Palm_closing = Closing("MP2/Palm.bmp", SE) * 250
Palm_boundary = Boundary("MP2/Palm.bmp", SE) * 250

# cv2.imshow("Palm_E", Palm_erosion)
# cv2.imshow("Palm_D", Palm_dilation)
# cv2.imshow("Palm_O", Palm_opening)
cv2.imshow("Palm_C", Palm_closing)
cv2.imshow("Palm_B", Palm_boundary)





cv2.waitKey(0)
cv2.destroyAllWindows()