
import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm



cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
direction = 0
form = 0
feedback = "Fix Form"


while cap.isOpened():
    ret, img = cap.read() #1280 x 720
    #Determine dimensions of video - Help with creation of box in Line 43
    width  = cap.get(3)  # float `width`
    height = cap.get(4)  # float `height`
    # print(width, height)
    
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        elbow = detector.findAngle(img, 11, 13, 15)
        shoulder = detector.findAngle(img, 13, 11, 23)
        hip = detector.findAngle(img, 11, 23,25)
        
        #Percentage of success of pushup
        per = np.interp(elbow, (90, 160), (0, 100))
        
        #Bar to show Pushup progress
        bar = np.interp(elbow, (90, 160), (380, 50))

        #Check to ensure right form before starting the program
        if elbow > 160 and shoulder > 40 and hip > 160:
            form = 1
    
        #Check for full range of motion for the pushup
        if form == 1:
            if per == 0:
                if elbow <= 90 and hip > 160:
                    feedback = "Up"
                    if direction == 0:
                        count += 0.5
                        direction = 1
                else:
                    feedback = "Fix Form"
                    
            if per == 100:
                if elbow > 160 and shoulder > 40 and hip > 160:
                    feedback = "Down"
                    if direction == 1:
                        count += 0.5
                        direction = 0
                else:
                    feedback = "Fix Form"
                        # form = 0
                
                    
    
        print(count)
        
        #Draw Bar
        if form == 1:
            cv2.rectangle(img, (1220, 50), (1240, 380), (255, 229, 204), 3)
            #cv2.rectangle(img, (0,0), (225,73), (193,255,193), -1)

            cv2.rectangle(img, (1220, int(bar)), (1240, 380), (255, 229, 204), cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (1200, 430), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                        (106, 106, 255), 2)


        #Pushup counter
        cv2.rectangle(img, (0, 0), (150, 73), (255, 229, 204), cv2.FILLED)
        cv2.putText(img, str(int(count)), (15, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 4,
                    (106, 106, 255), 4)
        
        #Feedback 
        cv2.rectangle(img, (520, 0), (760, 50), (255, 229, 204), cv2.FILLED)
        cv2.putText(img, feedback, (530, 40 ), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2,
                    (106, 106, 255), 2)

        
    cv2.imshow('Pushup counter', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
