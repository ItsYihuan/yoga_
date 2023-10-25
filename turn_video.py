import os
import cv2
from yoga_toolkit.yogaPose import YogaPose
CWD = os.getcwd().replace("\\","/")

video_path = f"{CWD}/yoga_toolkit/SampleVideo/ChildsPose/cc.mp4"
file_name = (video_path.split('/')[-1]).split('.')[0]
storage_path = f"{CWD}/yoga_toolkit/SampleVideo/SeatedForwardBendPose/{file_name}.mp4"
cap = cv2.VideoCapture(video_path)
original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
output = cv2.VideoWriter(storage_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (original_height,original_width))
print(original_width,original_height)
fps = cap.get(cv2.CAP_PROP_FPS)
while True:
    ret, frame = cap.read()
    if not ret:
        print("Video end")
        break
    # 水平翻轉影片
    frame = cv2.flip(frame, 180)
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow('image',frame)
    output.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
output.release()
cv2.destroyAllWindows()