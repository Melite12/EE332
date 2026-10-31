import cv2
import numpy as np
import math

from util import CannyEdgeDetector


def Parameterise(Edge, theta_quant, rho_quant):
    rows, cols = Edge.shape
    print(rows, cols)
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
    
    return parameterised_uint8
            


Test = CannyEdgeDetector("MP6/test.bmp")
Test2 = CannyEdgeDetector("MP6/test2.bmp")
Input = CannyEdgeDetector("MP6/input.bmp")

Test = Parameterise(Test, 256, 256)
Test2 = Parameterise(Test2, 256, 256)
Input = Parameterise(Input, 256, 256)

cv2.imshow("Test", Test)
cv2.imshow("Test2", Test2)
cv2.imshow("Input", Input)

# cv2.imwrite("MP6/Results/Test.bmp", Test)

cv2.waitKey(0)
cv2.destroyAllWindows()