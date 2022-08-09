import cv2
import mediapipe as mp
import numpy as np

# 시각화 할때 유용한 그리기 도구들
mp_drawing = mp.solutions.drawing_utils
# 포즈 추정 모델
mp_pose = mp.solutions.pose

# 영상 불러오기
cap = cv2.VideoCapture('squats1.mp4') 
# 웹캠 
#cap = cv2.VideoCapture(0) 


# 변수들
counter = 0
stage = None
stage2 = None
count = 0
direction = 0
feedback = ""
form = 1
cal = 0

# 화면 해상도
video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

## mediapipe 인스턴스 설정하기
## detection confidence, tracking confidence 동작을 더 정확하게 따고 싶으면 숫자를 올리면 됨 
## 하지만 tradeoff가 존재하기 때문에  0.5가 가장 적당하다고 판단
with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
    while cap.isOpened():
        # 영상에서 프레임 따오기
        ret, frame = cap.read()
        
        # 인지와 랜더딩 하기
        # Recolor image blue, green, red (RGB)
        # frame = feed from webcam or video, 후 reordering color 
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # false로 설정함으로써 메모리를 절약
        image.flags.writeable = False
        
        # 이미지에서 동작 감지
        results = pose.process(image)
        
        # 위에서 RGB로 바꾼거를 다시 BGR로 바꿔주기
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # 각도 계산하는 공식
        def calculate_angle(a, b, c):
            a = np.array(a) # 엉덩이 24
            b = np.array(b) # 무릎 16
            c = np.array(c) # 발목 138
            
            # calculate radians and  angle
            radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
            angle = np.abs(radians*180.0/np.pi)
            
            # 계산된 각도를 0에서 180도로 나오게 계산해 주기
            if angle > 180.0:
                angle = 360 - angle
                
            # 소숫점 지우기    
            return int(angle)
        
        # 랜드마크 발췌하기
        try:
            landmarks = results.pose_landmarks.landmark
            
            # 좌표 구하기 (대문자를 원하는 부위로 바꾸면 다른 3점 각도를 구할 수 있다)
            hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            
            shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            
            # 각도 계산하기
            angle = calculate_angle(hip, knee, ankle)
            angle2 = calculate_angle(shoulder, hip, knee)
            print(angle)
            print(angle2)
            # 각도 시각화
            cv2.putText(image, str(angle),
                            # 영상 해상도
                            tuple(np.multiply(knee, [video_width, video_height]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv2.LINE_AA
                        ) 
            
            cv2.putText(image, str(angle2),
                            tuple(np.multiply(hip, [video_width, video_height]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv2.LINE_AA
                        ) 
                         
            # 갯수 세는 로직
            if angle < 90:
                stage = "down"
                feedback = "Good job!"
            elif angle > 170 and stage == 'down':
                stage = "up"
                cal += 0.32
                counter += 1
                # feedback = "Good job!"
            else:
                feedback = "Bend your knees more" 
                
            # if angle2 < 50:
            #     stage2 = "down"
            # elif angle2 > 170 and stage2 == 'down':
            #     stage2 = "up"
            #     feedback = "Good job"
            # else:
            #     feedback = "Bend your knees more2"
                
            # print(cal)
            # print(counter)
                
        except:
            pass
        
        # 컬 카운터 렌더링
        # 정사각형 상자를 만들기
        # 상자를 넣고 싶은 이미지, 시작 좌표, 끝 좌표, 색, -1 은 색상으로 채우기
        cv2.rectangle(image, (0,0), (1000,200), (255, 229, 204), -1)
        
        cv2.rectangle(image, (0,210), (1000,350), (255, 229, 204), -1)

        
        # Rep data
        # 글씨를 넣고 싶은 곳, 글, 시작 좌표, 폰트, 사이즈, 색상, 선 두께, 선 타입
        cv2.putText(image, 'REPS', (15,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
        cv2.putText(image, str(counter),
                    (10,120),
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 2, cv2.LINE_AA)
        
        # Stage data 
        cv2.putText(image, 'STAGE', (200, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
        cv2.putText(image, stage,
                    (200,110),
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 2, cv2.LINE_AA)
        # 칼로리 소모량 계산
        cv2.putText(image, 'CALORIES BURNED', (600, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
        cv2.putText(image, str(cal) + 'cal',
                    (600,120),
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 2, cv2.LINE_AA)
        
        # 퍼센티치와 바 그래프
        # 퍼센트 각도, 시작 좌표, 0 ~ 100까지
        per = np.interp(angle, (80, 170), (0, 100))
        # 바 그래프 시작 좌표와 끝나는 좌표
        bar = np.interp(angle, (80, 170), (1800, 800))
        
        # 각도가 170이상 = 초기 상태 form이 1이라고 설정
        if angle > 170:
            form = 1
            
        #Check for full range of motion for the pushup
        # if form == 1:
        #     if per == 0:
        #         if angle >= 170:
        #             feedback = "Up"
        #             if direction == 0:
        #                 count += 0.5
        #                 direction = 1
        #         else:
        #             feedback = "Bend your knees more"
                    
        #     if per == 100:
        #         if angle < 80:
        #             feedback = "Down"
        #             if direction == 1:
        #                 count += 0.5
        #                 direction = 0
        #         else:
        #             feedback = "Bend your knees more"
        #                 # form = 0
        # print(count)
        
        #게이지 바 그리기
        if form == 1:
            cv2.rectangle(image, (70, 800), (180, 1800), (200, 229, 204), 3)
            
            cv2.rectangle(image, (70, int(bar)), (180, 1800), (255, 229, 204), cv2.FILLED)
            cv2.putText(image, f'{int(per)}%', (75, 1850), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2,
                         (106, 106, 255), 2)
                    
        #Feedback 
        cv2.putText(image, 'FEEDBACK', (0,250),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
        # cv2.putText(image, feedback, (1100, 110), cv2.FONT_HERSHEY_SIMPLEX, 2,
        #             (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, feedback, (0, 320), cv2.FONT_HERSHEY_SIMPLEX, 2,
                    (0, 0, 0), 2, cv2.LINE_AA)            
        
        # drawing utilites (mediapipe 이용)
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(239, 113, 38), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(128, 206, 185), thickness=2, circle_radius=2)
                                  )
        
        # 화면에 해당 프레임을 디스플레이
        cv2.imshow('Mediapipe Feed', image)

        # 종료하기
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
     
# 오픈한 cap 객체를 해제와 생성한 모든 윈도우 제거     
cap.release()
cv2.destroyAllWindows()
