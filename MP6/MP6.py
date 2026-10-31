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

    # for r in range(rows):
    #     for c in range(cols):
    #         if not Edge[r,c]:
    #             continue

            
    


Test = CannyEdgeDetector("MP6/test.bmp")
Test2 = CannyEdgeDetector("MP6/test2.bmp")
Input = CannyEdgeDetector("MP6/input.bmp")

Parameterise(Test, 10, 5)

# cv2.imshow("Test", Test)
# cv2.imshow("Test2", Test2)
# cv2.imshow("Input", Input)

# cv2.imwrite("MP6/Results/Test.bmp", Test)

# cv2.waitKey(0)
# cv2.destroyAllWindows()