import cv2
import sys
import time
import internals.poseModule as pm
from internals.poseType import PoseType
import internals.expectations as data


def calculate_progress(angle, angle_min, angle_max):
    angle = max(angle_max, min(angle, angle_min))
    progression = round(((angle - angle_min) / (angle_max - angle_min)) * 102)
    return progression


class Exercices:
    def __init__(self):
        self.pull_Up_Done = 0

    def start(self, workout):
        invert = data.fetchInvert(workout)
        title = data.fetchSugar(workout)
        # cap = cv2.VideoCapture(0)
        file = "assets/" + workout + ".mp4"
        cap = cv2.VideoCapture(file)
        detector = pm.poseDetector()
        pTime = 0
        self.reps = 0
        repDrop = False
        neededAngles = data.fetchAngles(workout)
        if invert:  # On inverse le système de comptage de rep selon que ce soit par exemple un squat ou une traction
            # TODO Faire plus que deux types de reward system et les refactoriser sur leur propre fichier
            # TODO ils retourneraint une fonction lambda qui permettrait de calculer la progression.
            def calculate_progress(angle, angleMin, angleMax):
                angle = max(angleMin, min(angle, angleMax))
                progression = round(((angle - angleMax) / (angleMin - angleMax)) * 100)
                return progression
        while True:
            sucess, img = cap.read()

            if sucess:
                img = detector.findPose(img, False)
                img = cv2.resize(img, (1024, 576))  # img = cv2.resize(img, (1280, 720))
                lmList = detector.findPosition(img, False)
                if len(lmList) != 0:
                    pose = self.poseHandler(img, detector, neededAngles)
                    expectations = data.lookup(workout, pose)
                    percentage = calculate_progress(*expectations[0])

                    if percentage >= 100 and repDrop == True:  # On ajoute une tolérance aussi..
                        self.reps += 1
                        repDrop = False
                    elif percentage == 0:
                        repDrop = True
                    # print(repDrop, percentage)
                    # print(f"{percentage}% | Pull up: {self.reps}")
                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv2.putText(img, str(int(fps)) + " fps", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 1)
                cv2.putText(img, f"{title}: {self.reps} reps", (800, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                cv2.imshow("B-PUMP", img)
                cv2.waitKey(1)
            else:
                cap.release()
                cv2.destroyAllWindows()
                sys.exit()

    def poseHandler(self, img, detector, joint_names):
        joint_indices = {
            "angleLeftArm": (12, 14, 16),
            "angleLeftHip": (12, 24, 26),
            "angleLeftLeg": (24, 26, 28),
            "angleLeftFoot": (26, 28, 32),
            "angleRightArm": (11, 13, 15),
            "angleRightHip": (11, 23, 25),
            "angleRightLeg": (23, 25, 27),
            "angleRightFoot": (25, 27, 31)
        }
        angles = [detector.findAngle(img, *joint_indices[joint]) for joint in joint_names]
        return PoseType(joint_names, angles)
