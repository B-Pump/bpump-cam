import cv2
import sys
import numpy as np
import time
import PoseModule as pm


def calculate_progress(angle, angle_min, angle_max):
    angle = max(angle_max, min(angle, angle_min))
    progression = round(((angle - angle_min) / (angle_max - angle_min)) * 100)
    return progression


class Exercices:

    def __init__(self):
        self.pull_Up_Done = 0


    def pull_Up(self):
        cap = cv2.VideoCapture("assets/pull-up.mp4") #cv2.VideoCapture(0) #<- Pour utilisé la camera
        detector = pm.poseDetector()
        pTime = 0
        self.pull_Up_Done = 0
        pullDrop = False

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
                    angle = detector.findAngle(img, 12, 24, 26)
                    angle = detector.findAngle(img, 24, 26, 28)

                    # Right side
                    angleRightArm = detector.findAngle(img, 11, 13, 15)
                    angle = detector.findAngle(img, 11, 23, 25)
                    angle = detector.findAngle(img, 23, 25, 27)

                    percentage = calculate_progress(angleLeftArm, 150, 48)

                    if percentage == 100 and pullDrop == True:
                        self.pull_Up_Done += 1
                        pullDrop = False
                    elif percentage == 0:
                        pullDrop = True

                    print(f"{percentage}% | Pull up: {self.pull_Up_Done}")

                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv2.putText(img, str(int(fps)) + " fps", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                cv2.putText(img, f"Pull up: {self.pull_Up_Done}", (800, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
                cv2.imshow("B-PUMP", img)
                cv2.waitKey(1)
            else:
                cap.release()
                cv2.destroyAllWindows()
                sys.exit()


