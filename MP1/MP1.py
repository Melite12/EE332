import cv2
import numpy as np

np.set_printoptions(threshold=np.inf)

img = cv2.imread("C:/Users/manas/OneDrive - Northwestern University/Northwestern/Quarters/Fall 2026/EE332/MP1/face.bmp", 0) # 0 loads it as grayscale

img = (img != 0).astype(np.uint8) # make img array into 1's and 0's instead of 255 and 0s
img_labelled = (np.zeros((img.shape[0],img.shape[1]))).astype(np.uint8)
img_relabelled = (np.zeros((img.shape[0],img.shape[1]))).astype(np.uint8)
set_list = []

L = 1
for u in range (img.shape[0]): 
    for v in range (img.shape[1]):
        if img[u][v] == 1:

            # Dealing with Row 0 / Column 0
            if u == 0:
                Lu = 0
            else:
                Lu = img_labelled[u-1][v]

            if v == 0:
                Ll = 0
            else:
                Ll = img_labelled[u][v-1]    

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

# recompiling the list of sets
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

    #print (supersets)
    if not merged_one:
        break

    set_list = supersets
    


# Second scanning using set_list
for u in range (img_labelled.shape[0]): 
    for v in range (img_labelled.shape[1]):
        val = img_labelled[u][v]

        if val != 0:
            for idx, s in enumerate(set_list):
                if val in s:
                    img_relabelled[u][v] = idx
                    break
  

# Output
img = img * 40
cv2.imshow("Face", img)

img_labelled = img_labelled * 4
cv2.imshow("Face2", img_labelled)

img_relabelled = img_relabelled * 40
cv2.imshow("Face3", img_relabelled)

cv2.waitKey(0)
cv2.destroyAllWindows()