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

def FindThreshold(Mag, percentageOfNonEdge):
    hist, bin_edges = np.histogram(Mag, bins=50) # make a histogram
    cumulative = np.cumsum(hist) # cumulative histogram
    threshold = cumulative[-1] * percentageOfNonEdge # the threshold of number of pixels
    bin_index = np.searchsorted(cumulative, threshold) # the index at which we get the threshold
    
    T_high = bin_edges[bin_index + 1] # calculate T_high as the bin_value at the next index in bin edges
    T_low = 0.5 * T_high

    return T_low, T_high

def LUT(angle):
    if angle < 22.5 or angle >= 157.5:
        offset = [[0,1], [0,-1]]
    elif angle < 67.5 or angle >= 112.5:
        offset = [[-1,1],[1,-1]]
    else:
        offset = [[-1,0],[1,0]]

    return offset


def NonmaximaSupress(Mag, Theta, method):

    rows, cols = Mag.shape
    angles = np.degrees(Theta) % 180
    result = np.zeros_like(Mag)

    match method:

        case 'Quantization':
            for r in range(1,rows-1):
                for c in range(1,cols-1):
                    offset = LUT(angles[r,c])
                    neighbour1 = (Mag[r + offset[0][0], c + offset[0][1]])
                    neighbour2 = (Mag[r + offset[1][0], c + offset[1][1]])
                    if Mag[r, c] >= neighbour1 and Mag[r, c] >= neighbour2:
                        result[r,c] = Mag[r, c]

        case 'Interpolation':
            result = result + 1

    return result

def Thresholding(Mag, T_high, T_low):
    strong_mask = Mag >= T_high
    weak_mask = Mag >= T_low

    strong = np.where(strong_mask, Mag, 0)
    weak = np.where(weak_mask, Mag, 0)

    return strong, weak

def EdgeLinking(Mag_low, Mag_high):



def CannyEdgeDetector(file):
    I = ReadImg(file)
    
    N = 3
    sigma = 1
    S = GaussSmoothing(I, N, sigma)
    
    Mag, Theta = ImageGradient(S)

    percentageOfNonEdge = 0.9
    T_low, T_high = FindThreshold(Mag, percentageOfNonEdge)

    Mag_surpress = NonmaximaSupress(Mag, Theta, 'Quantization')

    Mag_high, Mag_low = Thresholding(Mag_surpress, T_high, T_low)

    E = EdgeLinking(Mag_low, Mag_high)
    
    # high_display = (Mag_high > 0).astype(np.uint8) * 255
    # low_display = (Mag_low > 0).astype(np.uint8) * 255

    # cv2.imshow("High threshold", high_display)
    # cv2.imshow("Low threshold", low_display)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



CannyEdgeDetector("MP5/lena.bmp")
#cv2.imshow("Test", test)
#cv2.imwrite("MP4/Results/gun_rgb.bmp", gun1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


