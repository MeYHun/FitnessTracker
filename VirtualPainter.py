import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
header = overlayList[0]

cap = cv2.VideoCapture(0)
# 웹캠 resolution 설정하기
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon = 0.85)

while True:
    # 1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)
    
    # 2. Find Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = False)
    
    if len(lmList) != 0:
        print(lmList)
        
        # tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        
        
    
    # 3. Check which fingers are up (index finger = draw)
    # 4. If Selection Mode - Two fingers are up 
    # 5. If Drawing Mode - Index finger is up    
    
    
    
    
    
    # Setting the header image
    img[0:100, 0:1280] = header
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break