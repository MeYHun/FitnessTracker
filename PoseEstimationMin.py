import cv2
import mediapipe as mp
import numpy as np

# visualize 할때 drawing utilities
mp_drawing = mp.solutions.drawing_utils
# pose estimating model
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0) 

# Curl counter 변수들
counter = 0
stage = None


## setup mediapipe instance
## detection confidence, tracking confidence 더 정확하게 하고 싶으면 구체적 그럼 숫자 올리면 된다
## There is tradeoff 너무 높히면 model이 정확한 물체 못찾으면 오히려 안좋을 수 도
with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
    while cap.isOpened():
        # ret return variable, frame = 실제 영상 
        ret, frame = cap.read()
        
        # Detect stuff and render
        # Recolor image blue, green, red (RGB)
        # frame = feed from webcam 후 reordering color 
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # save memory by setting it false
        image.flags.writeable = False
        
        # Make detection
        results = pose.process(image)
        
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # 각도 계산하는 공식
        def calculate_angle(a, b, c):
            a = np.array(a) # First 11
            b = np.array(b) # Mid 13
            c = np.array(c) # End 15
            
            # calculate radians and  angle
            # 처음꺼는 y value
            radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
            angle = np.abs(radians*180.0/np.pi)
            
            # convert to angle between 0 ~ 180 degree
            if angle > 180.0:
                angle = 360 - angle
                
            return angle
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # 좌표 구하기 (대문자를 원하는 부위로 바꾸면 다른 3점 각도를 구할 수 있다)
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            # 각도 계산하기
            angle = calculate_angle(shoulder, elbow, wrist)
            print(angle)
            # 각도 시각화
            cv2.putText(image, str(angle),
                            # demension of the webcam
                            tuple(np.multiply(elbow, [1280, 720]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        ) 
                         
            # Curl counter logic
            if angle > 160:
                stage = "down"
            if angle < 30 and stage == 'down':
                stage = "up"
                counter += 1
                print(counter)
                
        except:
            pass
        
        # Render curl counter
        # Setup status box
        # 상자를 넣고 싶은 이미지, start point, end point, color, fill in with color
        cv2.rectangle(image, (0,0), (225,73), (193,255,193), -1)
        
        # Rep data
        # 15,12 시작 coordinate
        # font, size of text, color, line width, line width type
        cv2.putText(image, 'REPS', (15,12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter),
                    (10,60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Stage data
        cv2.putText(image, 'STAGE', (65, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, stage,
                    (60,60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # 게이지 바  그기
        
                    
                    
                    
        # Render detections
        # drawing utilites (mediapipe가 해준다)
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(239, 113, 38), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(128, 206, 185), thickness=2, circle_radius=2)
                                  )
        
        cv2.imshow('Mediapipe Feed', image)

        # feed clear 했을때/ 화면 지우는거
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
    
        
cap.release()
cv2.destroyAllWindows()

