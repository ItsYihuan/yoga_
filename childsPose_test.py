import os
import cv2
import mediapipe as mp
CWD = os.getcwd().replace("\\","/")

mp_drawing = mp.solutions.drawing_utils          # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_pose = mp.solutions.pose                      # mediapipe 姿勢偵測

# # detect video path
video_path = f"{CWD}/yoga_toolkit/SampleVideo/ChildsPose/sample.mp4"
file_name = (video_path.split('/')[-1]).split('.')[0]
storage_path = f"{CWD}/yoga_toolkit/SampleVideo/ChildsPose/output.mp4"

cap = cv2.VideoCapture(video_path)
original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
output = cv2.VideoWriter(storage_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (original_width, original_height))
print(original_width,original_height)
fps = cap.get(cv2.CAP_PROP_FPS)

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
    # Import video file
        video_cap = cv2.VideoCapture(video_path)

        if (video_cap.isOpened()== False): 
            print("Error opening video  file")

        success, image = video_cap.read()

        if success:
            print("success")
        while True:
            ret, img = cap.read()
            if not ret:
                print("Cannot receive frame")
                break
            #img = cv2.resize(img,(520,300))               # 縮小尺寸，加快演算速度
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # 將 BGR 轉換成 RGB
            results = pose.process(img2)                  # 取得姿勢偵測結果
            # 根據姿勢偵測結果，標記身體節點和骨架
            mp_drawing.draw_landmarks(
                img,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            cv2.imshow('oxxostudio', img)
            output.write(img)
            if cv2.waitKey(5) == ord('q'):
                break     # 按下 q 鍵停止
    
cap.release()
output.release()
cv2.destroyAllWindows()