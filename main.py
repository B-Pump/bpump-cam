import cv2
import sys
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture("assets/pull-up.mp4")
detector = pm.poseDetector()
pTime = 0

while True:
    sucess, img = cap.read()

    if sucess:
        img = detector.findPose(img, False)
        img = cv2.resize(img, (1280, 720))
        lmList = detector.findPosition(img, False)
        # print(lmList)

        if len(lmList) != 0:
            angle = detector.findAngle(img, 12, 14, 16)
            angle = detector.findAngle(img, 12, 24, 26)
            angle = detector.findAngle(img, 24, 26, 28)

            percentage = np.interp(angle, (210, 310), (0, 100))
            # print(angle, percentage)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)) + " fps", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

        cv2.imshow("B-PUMP", img)
        cv2.waitKey(1)
    else:
        cap.release()
        cv2.destroyAllWindows()
        sys.exit()