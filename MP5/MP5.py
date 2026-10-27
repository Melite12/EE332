import cv2
import numpy as np
import math

def ReadImg(I):
    Out = cv2.imread(I)
    Out = cv2.cvtColor(Out, cv2.COLOR_BGR2GRAY)
    Out = Out.astype(np.float64)
    return Out

def GaussSmoothing(I, N, sigma):
    gaussian_1d = cv2.getGaussianKernel(N, sigma)
    gaussian_2d = gaussian_1d @ gaussian_1d.T

    S = cv2.filter2D(I, -1, gaussian_2d) # you can change boundary using borderType = cv2.BORDER_REPLICATE / REFLECT / CONSTANT
    S = S / 255
    return S

def ImageGradient(S):
    SobelX = np.array([[-1, 0, 1],
                       [-2, 0, 2],
                       [-1, 0, 1]], dtype=float)

    SobelY = np.array([[1, 2, 1],
                       [0, 0, 0],
                       [-1, -2, -1]], dtype=float)

    Gx = cv2.filter2D(S, -1, SobelX)
    Gy = cv2.filter2D(S, -1, SobelY)
    Mag = np.sqrt(Gx**2, Gy**2)
    Theta = np.arctan2(Gy, Gx)

    # print(Mag)
    # print(Mag.shape)
    # print(Theta)
    # print(Theta.shape)
    return Mag, Theta

def CannyEdgeDetector(file):
    I = ReadImg(file)
    N = 3
    sigma = 1
    S = GaussSmoothing(I, N, sigma)
    Mag, Theta = ImageGradient(S)

    # Mag_display = cv2.normalize(Mag, None, 0, 255, cv2.NORM_MINMAX)
    # Mag_display = Mag_display.astype("uint8")

    # cv2.imshow("Gradient magnitude", Mag_display)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


CannyEdgeDetector("MP5/lena.bmp")
#cv2.imshow("Test", test)
#cv2.imwrite("MP4/Results/gun_rgb.bmp", gun1)
cv2.waitKey(0)
cv2.destroyAllWindows()


