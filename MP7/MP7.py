import cv2
import numpy as np
import math
import os

class Video:
    def __init__(self, image_folder, video):
        self.image_folder = image_folder
        self.video = video
        filenames = sorted([
            img for img in os.listdir(image_folder) 
            if img.lower().endswith(".jpg")
        ])
        self.images = [
            cv2.imread(os.path.join(image_folder, img))
            for img in filenames
        ]
        self.height, self.width = self.images[0].shape[:2]

def CreateVideo(Video, fps):

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'XVID' for .avi files
    video = cv2.VideoWriter(Video.video, fourcc, fps, (Video.width, Video.height))

    for image in Video.images:
        video.write(image)

    video.release()
    print("Video created successfully!")

def SSD(Video, top_left, bottom_right, delta):

    # Convert to grayscale
    prev_img_colour = Video.images[0]
    prev_img = cv2.cvtColor(prev_img_colour, cv2.COLOR_BGR2GRAY)

    total_delta = 2 * delta + 1
    col_start = top_left[0] - delta
    col_end = col_start + total_delta
    row_start = top_left[1] - delta
    row_end = row_start + total_delta
    print(col_start, row_start)
    
    for img in range(1,len(Video.images)):
        curr_img_colour = Video.images[img]
        curr_img = cv2.cvtColor(curr_img_colour, cv2.COLOR_BGR2GRAY)

        for c in range(col_start, col_end):
            for r in range(row_start, row_end):
                # compute SSD
                # if it's lowest, then keep the value

        # create new image with new bounding box
        # add the image to results folder
    
    # make a video from the folder
    # return the top_left, bottom_right?

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

    # SSD Target Tracking
    delta = 10
    SSD(Girl_video, top_left, bottom_right, delta)


TargetTracking()

# cv2.imshow("First Image", first_frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()







