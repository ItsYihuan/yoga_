import os
import threading
import time
import cv2
from yoga_toolkit.yogaPose import YogaPose
from yoga_toolkit.mat_data import *
""" Turn off the comment below if the yoga mat is connected. """
use_mat = True
if(use_mat):
	from yoga_toolkit.yogamat import get_heatmap

CWD = os.getcwd().replace("\\", "/")

# IMAGE_FILES = [f"{CWD}/yoga_toolkit/TreePose/Image/detect/test.jpg",
#                f"{CWD}/yoga_toolkit/TreePose/Image/detect/test4.jpg",
#                f"{CWD}/yoga_toolkit/TreePose/Image/detect/test5.jpg"]

'''
type: WarriorII, Tree, Plank, ReversePlank, Childs, DownwardDog, LowLunge, SeatedForwardBend, Bridge, Pyramid
'''
pose = YogaPose("Tree")
pose.initialDetect()

# # detect video path
video_path = f"{CWD}/yoga_toolkit/SampleVideo//TreePose/sample.mp4"
file_name = (video_path.split('/')[-1]).split('.')[0]
storage_path = f"{CWD}/yoga_toolkit/SampleVideo//TreePose/output/{file_name}.mp4"

cap = cv2.VideoCapture(video_path)
original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
output = cv2.VideoWriter(storage_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (original_width, original_height))
print(original_width, original_height)
fps = cap.get(cv2.CAP_PROP_FPS)

yoga_mat_data = mat_data()

def cap_update():
    """
    This is a function used to update the frame of the camera.
    """
    global yoga_mat_data
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Video end")
            break
        frame = pose.detect(frame, original_width, original_height, False, yoga_mat_data)
        # 水平翻轉影片
        frame = cv2.flip(frame, 180)
        print(pose.tips)
        cv2.imshow('image', frame)
        output.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def get_mat_data():
    global yoga_mat_data

    if (use_mat):
        while True:
            heatmap_frame, yoga_mat_data = get_heatmap()
            cv2.imshow("heatmap", heatmap_frame)
            # print(yoga_mat_data)
            if cv2.waitKey(1) == ord('q'):
                break

get_mat_data_thread = threading.Thread(target=get_mat_data, daemon=True)
web_thread = threading.Thread(target=cap_update, daemon=True)


get_mat_data_thread.start()
web_thread.start()

web_thread.join()

cap.release()
output.release()
cv2.destroyAllWindows()