import cv2
import numpy as np

np.set_printoptions(threshold=np.inf)

img = cv2.imread("C:/Users/manas/OneDrive - Northwestern University/Northwestern/Quarters/Fall 2026/EE332/MP1/face.bmp", 0) # 0 loads it as grayscale
#print(img[20:40]) # numpy array
#print(img.shape) #(height, width)

img = (img != 0).astype(np.uint8) # make img array into 1's and 0's instead of 255 and 0s
print(img[20:40])

for u in range (img.shape[0]): 
    for v in range (img.shape[1]):
        Lu = img[u-1][v]
        Ll = img[u][v-1]     

img = img * 40
cv2.imshow("Face", img)
cv2.waitKey(0)
cv2.destroyAllWindows()