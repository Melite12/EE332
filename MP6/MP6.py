import cv2
import numpy as np
import math

from util import CannyEdgeDetector


def Parameterise(Edge, theta_quant, rho_quant):
    rows, cols = Edge.shape
    parameterised = np.zeros((theta_quant, rho_quant), dtype=int)
    
    theta_bound = math.pi/2
    theta_arr = np.arange(-theta_bound, theta_bound, (2*theta_bound)/theta_quant)
    rho_bound = math.sqrt(rows**2 + cols**2)
    rho_arr = np.arange(-rho_bound, rho_bound, (2*rho_bound) / rho_quant)

    for r in range(rows):
        for c in range(cols):

            if not Edge[r,c]:
                continue

            for theta_idx, theta in enumerate(theta_arr):
                rho = c*math.cos(theta) + r*math.sin(theta)
                rho_idx = np.abs(rho_arr - rho).argmin()
                parameterised[theta_idx, rho_idx] += 1

    parameterised_uint8 =  (parameterised / (np.max(parameterised) / 255)).astype(np.uint8)

    return parameterised_uint8, theta_arr, rho_arr

def sig_intersection(parameterised_uint8, threshold):
    
    # Thresholding
    threshold_val = threshold * np.max(parameterised_uint8)

    # Non-maxima Surpression
    size = 50
    mat = np.ones((size, size), np.uint8)

    local_max = cv2.dilate( parameterised_uint8, mat)
    peaks = ((parameterised_uint8 == local_max) & (parameterised_uint8 > threshold_val))
    theta_idx, rho_idx = np.where(peaks)
    print(theta_idx.shape, rho_idx.shape)

    return theta_idx, rho_idx

def LineDetection(file):

    Edge = CannyEdgeDetector(file)

    theta_quant = 256
    rho_quant = 256
    parameterised_uint8, theta_arr, rho_arr = Parameterise(Edge, theta_quant, rho_quant)

    threshold = 0.45
    theta_idx, rho_idx = sig_intersection(parameterised_uint8, threshold)

    output = cv2.imread(file)

    for theta_idx1, rho_idx1 in zip(theta_idx, rho_idx):
        theta = theta_arr[theta_idx1]
        rho = rho_arr[rho_idx1]

        x0 = rho * np.cos(theta)
        y0 = rho * np.sin(theta)

        dist = 400
        x1 = int(x0 - dist * np.sin(theta))
        y1 = int(y0 + dist * np.cos(theta))

        x2 = int(x0 + dist * np.sin(theta))
        y2 = int(y0 - dist * np.cos(theta))

        cv2.line(output, (x1, y1), (x2, y2), (150, 150, 150), 1)

    cv2.imshow("Detected Lines", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


Test = LineDetection("MP6/test.bmp")
Test2 = LineDetection("MP6/test2.bmp")
Input = LineDetection("MP6/input.bmp")

cv2.imshow("Test", Test)
cv2.imshow("Test2", Test2)
cv2.imshow("Input", Input)

# cv2.imwrite("MP6/Results/Test.bmp", Test)

cv2.waitKey(0)
cv2.destroyAllWindows()