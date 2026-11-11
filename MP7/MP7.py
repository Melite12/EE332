import cv2
import numpy as np
import math
import os

class Video:
    def __init__(self, image_folder, video_folder):
        self.image_folder = image_folder
        self.video_folder = video_folder
        filenames = sorted([
            img for img in os.listdir(image_folder) 
            if img.lower().endswith(".jpg")
        ])
        self.images = [
            cv2.imread(os.path.join(image_folder, img))
            for img in filenames
        ]
        self.height, self.width = self.images[0].shape[:2]

def CreateVideo(Video_input, fps):

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'XVID' for .avi files
    video = cv2.VideoWriter(Video_input.video_folder, fourcc, fps, (Video_input.width, Video_input.height))

    for image in Video_input.images:
        video.write(image)

    video.release()
    print("Video created successfully!")

def Matching(Video_input, top_left, bottom_right, delta, mode):

    box_width = bottom_right[0] - top_left[0]
    box_height = bottom_right[1] - top_left[1]

    total_delta = 2 * delta + 1

    match mode:
        case 0:
            folder = "Results"
            name = "SSD"
        case 1:
            folder = "CC"
            name = "CC"
        case 2:
            folder = "NCC"
            name = "NCC"

    for img in range(1, len(Video_input.images)):

        prev_img = cv2.cvtColor(Video_input.images[img - 1], cv2.COLOR_BGR2GRAY)
        curr_img = cv2.cvtColor(Video_input.images[img], cv2.COLOR_BGR2GRAY)

        prev_col = top_left[0]
        prev_row = top_left[1]

        col_start = prev_col - delta
        row_start = prev_row - delta

        T = prev_img[prev_row:prev_row + box_height, prev_col:prev_col + box_width].astype(np.float64)

        best_c = None
        best_r = None
        if mode == 0 :
            best_err = math.inf
        else:
            best_err = -math.inf

        for c in range(total_delta):
            for r in range(total_delta):

                candidate_col = col_start + c
                candidate_row = row_start + r

                if (candidate_col < 0 or candidate_row < 0 or
                    candidate_col + box_width > Video_input.width or
                    candidate_row + box_height > Video_input.height):
                    continue

                I = curr_img[candidate_row:candidate_row + box_height, candidate_col:candidate_col + box_width].astype(np.float64)

                match mode:
                    case 0:
                        err = np.sum((I - T) ** 2)
                        if err < best_err:
                            best_err = err
                            best_c = candidate_col
                            best_r = candidate_row
                    case 1:
                        err = np.sum(I * T) # but want to maximise
                        if err > best_err:
                            best_err = err
                            best_c = candidate_col
                            best_r = candidate_row
                    case 2:
                        I_norm = I - np.mean(I)
                        T_norm = T - np.mean(T)

                        numerator = np.sum(I_norm * T_norm)
                        denominator = np.sqrt(np.sum(I_norm**2) * np.sum(T_norm**2))

                        err = numerator / denominator if denominator > 0 else -np.inf

                        if err > best_err:
                            best_err = err
                            best_c = candidate_col
                            best_r = candidate_row
                        

        top_left = (best_c, best_r)
        bottom_right = (best_c + box_width, best_r + box_height)
        # make the image and put it in results
        modified_img = Video_input.images[img].copy()
        cv2.rectangle(modified_img, top_left, bottom_right, (200,0,0), 2)
        cv2.imwrite(f"MP7/{folder}/{img:03d}.jpg", modified_img)

    Output_video = Video(f"MP7/{folder}", f"MP7/{name}.mp4")    
    CreateVideo(Output_video, 10)
    

def TargetTracking():
    Girl_video = Video("MP7/image_girl", "MP7/image_girl.mp4")
    fps = 10

    # Create Initial Video
    CreateVideo(Girl_video, fps)

    # Make an initial box on the first frame
    first_frame = Girl_video.images[0]
    modified_img = first_frame.copy()
    top_left = (50, 18)
    bottom_right = (93, 68)
    modified_img = cv2.rectangle(modified_img, top_left, bottom_right, (200,0,0), 2)

    cv2.imwrite(f"MP7/Results/000.jpg", modified_img)
    cv2.imwrite(f"MP7/CC/000.jpg", modified_img)
    cv2.imwrite(f"MP7/NCC/000.jpg", modified_img)
    
    # Target Tracking
    delta = 20
    Matching(Girl_video, top_left, bottom_right, delta, 2)



TargetTracking()

# cv2.imshow("First Image", first_frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()