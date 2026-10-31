import cv2
import numpy as np
import math

from util import CannyEdgeDetector












Test = CannyEdgeDetector("MP6/test.bmp")
Test2 = CannyEdgeDetector("MP6/test2.bmp")
Input = CannyEdgeDetector("MP6/input.bmp")
cv2.imshow("Test", Test)
cv2.imshow("Test2", Test2)
cv2.imshow("Input", Input)

# cv2.imwrite("MP6/Results/Test.bmp", Test)

cv2.waitKey(0)
cv2.destroyAllWindows()