import mediapipe as mp
import cv2

mp_drawing = mp.solutions.drawing_utils          # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_pose = mp.solutions.pose                      # mediapipe 姿勢偵測

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
    img = cv2.imread("./data/image/Childs/yoga_sample.png")

    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img2)                  # 取得姿勢偵測結果
    print(results.pose_landmarks)
    mp_drawing.draw_landmarks(
            img,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    cv2.imshow('label',img)
    cv2.waitKey(0)
