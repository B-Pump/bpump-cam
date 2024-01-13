import cv2
import sys
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture("assets/curl.mp4")
detector = pm.poseDetector()
pTime = 0

curlDone = 0
curlDrop = False

def calculate_progress(angle, angleMin, angleMax):
    angle = max(angleMin, min(angle, angleMax))
    progression = round(((angle - angleMax) / (angleMin - angleMax)) * 100)
    return progression


while True:
    sucess, img = cap.read()

    if sucess:
        img = detector.findPose(img, False)
        img = cv2.resize(img, (1024, 576)) #img = cv2.resize(img, (1280, 720))
        lmList = detector.findPosition(img, False)
        # print(lmList)

        if len(lmList) != 0:
            # Left side
            angleLeftArm = detector.findAngle(img, 12, 14, 16)
            angleLeftUpperLeg = detector.findAngle(img, 12, 24, 26)
            angleLeftLowerLeg = detector.findAngle(img, 24, 26, 28)

            # Right side
            angleRightArm = detector.findAngle(img, 11, 13, 15)
            angleRightUpperLeg = detector.findAngle(img, 11, 23, 25)
            angleRightLowerLeg = detector.findAngle(img, 23, 25, 27)

            percentageLeft = calculate_progress(angleLeftArm, 70, 160)
            percentageRight = calculate_progress(angleLeftArm, 70, 160)

            if percentageLeft == 100 and percentageRight == 100 and curlDrop == True:
                curlDone += 1
                curlDrop = False
            elif percentageLeft == 0 and percentageRight == 0:
                curlDrop = True

            print(f"{percentageLeft}% et {percentageRight}% | Pull up: {curlDone}")

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)) + " fps", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        cv2.putText(img, f"Curl: {curlDone}", (800, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
        cv2.imshow("B-PUMP", img)
        cv2.waitKey(1)
    else:
        cap.release()
        cv2.destroyAllWindows()
        sys.exit()