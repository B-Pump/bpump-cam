import cv2
import sys
import time
import PoseModule as pm

cap = cv2.VideoCapture("assets/walk.mp4")
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
        img = detector.findPose(img, True)
        img = cv2.resize(img, (1024, 576)) #img = cv2.resize(img, (1280, 720))
        lmList = detector.findPosition(img, False)
        # print(lmList)

        if len(lmList) != 0:
            # Left side
            angleLeftArm = detector.findAngle(img, 12, 14, 16)
            angleLeftHip = detector.findAngle(img, 12, 24, 26)
            angleLeftLeg = detector.findAngle(img, 24, 26, 28)
            angleLeftFoot = detector.findAngle(img, 26, 28, 32)

            # Right side
            angleRightArm = detector.findAngle(img, 11, 13, 15)
            angleRightHip = detector.findAngle(img, 11, 23, 25)
            angleRightLeg = detector.findAngle(img, 23, 25, 27)
            angleRightFoot = detector.findAngle(img, 25, 27, 31)

            percentageLeftHip = calculate_progress(angleRightHip, 50, 160)
            percentageRightHip = calculate_progress(angleRightHip, 50, 160)

            if percentageLeftHip == 100 and percentageRightHip == 100 and curlDrop == True:
                curlDone += 1
                curlDrop = False
            elif percentageLeftHip == 0 and percentageRightHip == 0:
                curlDrop = True

            print(f"{percentageLeftHip}% et {percentageRightHip}% | Pull up: {curlDone}")

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