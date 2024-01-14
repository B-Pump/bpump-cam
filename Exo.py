import cv2
import sys
import time
import internals.poseModule as pm
from internals.poseType import PoseType
import internals.expectations as data
def calculate_progress(angle, angle_min, angle_max):
    angle = max(angle_max, min(angle, angle_min))
    progression = round(((angle - angle_min) / (angle_max - angle_min)) * 100)
    return progression


class Exercices:
    def __init__(self):
        self.pull_Up_Done = 0

    def start(self, workout):
        cap = cv2.VideoCapture(0)  # VideoCapture("assets/pull-up.mp4") #cv2.VideoCapture(0) #<- Pour utilisé la camera
        detector = pm.poseDetector()
        pTime = 0
        self.reps = 0
        repDrop = False

        while True:
            sucess, img = cap.read()

            if sucess:
                img = detector.findPose(img, False)
                img = cv2.resize(img, (1024, 576)) #img = cv2.resize(img, (1280, 720))
                lmList = detector.findPosition(img, False)
                if len(lmList) != 0:
                    pose = self.poseHandler(detector, img)
                    expectations = data.lookup(workout, pose)
                    percentage = calculate_progress(*expectations[0])

                    if percentage == 100 and repDrop == True:
                        self.reps += 1
                        repDrop = False
                    elif percentage == 0:
                        repDrop = True

                    # print(f"{percentage}% | Pull up: {self.reps}")
                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv2.putText(img, str(int(fps)) + " fps", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                cv2.putText(img, f"{workout}: {self.reps}", (800, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                cv2.imshow("B-PUMP", img)
                cv2.waitKey(1)
            else:
                cap.release()
                cv2.destroyAllWindows()
                sys.exit()

    def poseHandler(self, detector, img):
        joints = [(12, 14, 16), (12, 24, 26,), (24, 26, 28), (11, 13, 15), (11, 23, 25), (23, 25, 27)]
        angles = [detector.findAngle(img, *j) for j in joints]
        left_side_joints = [(12, 14, 16), (12, 24, 26), (24, 26, 28), (26, 28, 32)]
        right_side_joints = [(11, 13, 15), (11, 23, 25), (23, 25, 27), (25, 27, 31)]
        left_side_angles = [detector.findAngle(img, *j) for j in left_side_joints]
        right_side_angles = [detector.findAngle(img, *j) for j in right_side_joints]
        all_angles = left_side_angles + right_side_angles
        # TODO AU LIEU DE COMPUTER TOUS LES ANGLES, TROUVER CEUL CEUX QU'ON A BESOIN
        return PoseType(angles, all_angles)
