import os
import cv2
import mediapipe as mp
import math as m

def computeAngle(point1, centerPoint, point2):
    """compute joint poins angle

    Args:
        point1 (list): joint points contains x,y,z
        centerPoint (list): joint points contains x,y,z
        point2 (list): joint points contains x,y,z

        centerPoint--->point1 = vector1
        centerPoint--->point2 = vector2
        use vector1 & vector2 compute angle

    Returns:
        degree (float)
    """
    p1_x, pc_x, p2_x = point1[0], centerPoint[0], point2[0]
    p1_y, pc_y, p2_y = point1[1], centerPoint[1], point2[1]

    if len(point1) == len(centerPoint) == len(point2) == 3:
        # 3 dim
        p1_z, pc_z, p2_z = point1[2], centerPoint[2], point2[2]
    else:
        # 2 dim
        p1_z, pc_z, p2_z = 0,0,0

    # vector
    x1,y1,z1 = (p1_x-pc_x),(p1_y-pc_y),(p1_z-pc_z)
    x2,y2,z2 = (p2_x-pc_x),(p2_y-pc_y),(p2_z-pc_z)

    # angle
    cos_b = (x1*x2 + y1*y2 + z1*z2) / (m.sqrt(x1**2 + y1**2 + z1**2) *(m.sqrt(x2**2 + y2**2 + z2**2)))
    B = m.degrees(m.acos(cos_b))
    return B
def getLandmarks(landmark, w=500, h=500):
    """Get skeleton landmark x,y,z respectively

    Args:
        landmark (mediapipe landmark): skeleton landmark
        w (int): image w
        h (int): image h

    Returns:
        2D relative coordinates(image) landmark(x,y) || 3D real coordinates landmark(x,y,z)

    """
    if w == None or h == None:
        return landmark.x, landmark.y, landmark.z
    else:
        return int(landmark.x*w), int(landmark.y*h)
CWD = os.getcwd().replace("\\","/")

mp_drawing = mp.solutions.drawing_utils          # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_pose = mp.solutions.pose                      # mediapipe 姿勢偵測



# # detect video path
video_path = f"{CWD}/yoga_toolkit/SampleVideo/BridgePose/sample.mp4"
file_name = (video_path.split('/')[-1]).split('.')[0]
storage_path = f"{CWD}/yoga_toolkit/SampleVideo/BridgePose/output.mp4"

cap = cv2.VideoCapture(video_path)
original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
output = cv2.VideoWriter(storage_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (original_width, original_height))
print(original_width,original_height)
fps = cap.get(cv2.CAP_PROP_FPS)

with mp_pose.Pose(
    min_detection_confidence=0.4,
    min_tracking_confidence=0.4) as pose:
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
            
            BRIDGE_ANGLE = {
                "LEFT_ELBOW": [results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER], results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW], results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]],
                "RIGHT_ELBOW": [results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER], results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW], results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]],
                "LEFT_SHOULDER": [results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW], results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER], results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]],
                "RIGHT_SHOULDER": [results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW], results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER], results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]],
                "LEFT_HIP": [results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER], results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP], results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]],
                "RIGHT_HIP": [results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER], results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP], results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]],
                "LEFT_KNEE": [results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP], results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE], results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]],
                "RIGHT_KNEE": [results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP], results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE], results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]],
                "LEFT_ANKLE": [results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE], results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE], results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX]],
                "RIGHT_ANKLE": [results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE], results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE], results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]],
            }

            angle_dict={}
            for key,value in BRIDGE_ANGLE.items():
                angle = computeAngle(list(getLandmarks(value[0],original_width,original_height)),
                    list(getLandmarks(value[1],original_width,original_height)),
                    list(getLandmarks(value[2],original_width,original_height)))
                angle_dict[key] = angle
            print(angle_dict)
            
            cv2.imshow('oxxostudio', img)
            output.write(img)
            if cv2.waitKey(5) == ord('q'):
                break     # 按下 q 鍵停止
    
cap.release()
output.release()
cv2.destroyAllWindows()