import cv2
import numpy as np
import math

def find_set(set_list, val):
    for idx, s in enumerate(set_list):
        if val in s:
            return idx

def sequentialCCL(filename, size_filter):

    img = cv2.imread(filename, 0) 
        # 0 loads it as grayscale

    # Initialising images and sets
    img = (img != 0).astype(np.uint8) # make img array into 1's and 0's instead of 255 and 0s
    img_labelled = (np.zeros((img.shape[0],img.shape[1]))).astype(np.uint8) # for first pass
    set_list = []

    L = 1
    for u in range (img.shape[0]): 
        for v in range (img.shape[1]):
            if img[u][v] == 1:

                # Dealing with Row 0 / Column 0
                Lu = 0 if u == 0 else img_labelled[u-1][v]
                Ll = 0 if v == 0 else img_labelled[u][v-1]    

                # Main logic of sequential CCL
                if Lu == Ll and Lu != 0:
                    new = Lu
                elif (bool(Lu) ^ bool(Ll)):
                    new = max(Lu, Ll)
                elif Lu != Ll and (Lu and Ll):
                    new = min(Lu, Ll)

                    i = find_set(set_list, Lu)
                    j = find_set(set_list, Ll)
                    if i != j:
                        set_list[i] |= set_list[j]
                        del set_list[j]

                else:
                    new = L
                    set_list.append({L})
                    L += 1
                
                img_labelled[u][v] = new

    num_labels = len(set_list)
    sizes = np.zeros(num_labels)

    # Second scan using set_list
    for u in range (img_labelled.shape[0]): 
        for v in range (img_labelled.shape[1]):
            val = img_labelled[u][v]

            if val != 0:
                for idx, s in enumerate(set_list):
                    if val in s:
                        img_labelled[u][v] = idx + 1
                        sizes[idx] += 1
                        break

    # Size Filter
    if size_filter:
        sizes = (sizes < size_filter)
        for u in range (img_labelled.shape[0]): 
            for v in range (img_labelled.shape[1]):
                val = img_labelled[u][v]
                if val and sizes[val - 1]:
                    img_labelled[u][v] = 0


    scale = math.floor(255 / num_labels)
    img_labelled = img_labelled * scale
    
    return img_labelled, num_labels

filter = 100
test, num_test = sequentialCCL("MP1/test.bmp", 0)
face, num_face = sequentialCCL("MP1/face.bmp", 0)
gun, num_gun = sequentialCCL("MP1/gun.bmp", 0)

test_filter, num_test = sequentialCCL("MP1/test.bmp", filter)
face_filter, num_face = sequentialCCL("MP1/face.bmp", filter)
gun_filter, num_gun = sequentialCCL("MP1/gun.bmp", filter)

cv2.imshow("Test", test)
cv2.imshow("Face", face)
cv2.imshow("Gun", gun)

cv2.imwrite("MP1/Results/test_labelled.bmp", test)
cv2.imwrite("MP1/Results/face_labelled.bmp", face)
cv2.imwrite("MP1/Results/gun_labelled.bmp", gun)

cv2.imwrite("MP1/Results/test_labelled_filter.bmp", test_filter)
cv2.imwrite("MP1/Results/face_labelled_filter.bmp", face_filter)
cv2.imwrite("MP1/Results/gun_labelled_filter.bmp", gun_filter)


cv2.waitKey(0)
cv2.destroyAllWindows()