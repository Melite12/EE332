import cv2
import numpy as np
import math

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
                elif Lu != Ll and not(Lu and Ll):
                    new = max(Lu, Ll)
                elif Lu != Ll and (Lu and Ll):
                    new = min(Lu, Ll)
                    set_list.append({Lu,Ll})
                else:
                    new = L
                    L += 1
                
                img_labelled[u][v] = new


    # Recompiling the list of sets
    while True:
        merged_one = False
        supersets = [set_list[0]]

        for s in set_list[1:]:
            in_super_set = False
            for ss in supersets:
                if s & ss:
                    ss |= s
                    merged_one = True
                    in_super_set = True
                    break

            if not in_super_set:
                supersets.append(s)

        if not merged_one:
            break

        set_list = supersets
    num_labels = len(set_list)


    # Second scan using set_list
    for u in range (img_labelled.shape[0]): 
        for v in range (img_labelled.shape[1]):
            val = img_labelled[u][v]

            if val != 0:
                for idx, s in enumerate(set_list):
                    if val in s:
                        img_labelled[u][v] = idx + 1
                        break

    scale = math.floor(255 / num_labels)
    img_labelled = img_labelled * scale
    
    return img_labelled, num_labels
  
test, num_test = sequentialCCL("MP1/test.bmp", 0)
face, num_face = sequentialCCL("MP1/face.bmp", 0)
gun, num_gun = sequentialCCL("MP1/gun.bmp", 0)

cv2.imshow("Test", test)
cv2.imshow("Face", face)
cv2.imshow("Gun", gun)

cv2.waitKey(0)
cv2.destroyAllWindows()