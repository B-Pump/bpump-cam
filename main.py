import cv2
import time
import internals.poseModule as pm
from internals.poseType import PoseType
import internals.expectations as data

class Exercices:
    def __init__(self):
        """
        Class initialization
        """
        pass

    def start(self, workout, reps):
        """
        Start the specified exercise

        :param workout: The name of the exercise
        :param reps: The number of repetitions to perform
        :return: The number of repetitions performed
        """
        invert = data.fetchInvert(workout)
        title = data.fetchSugar(workout)
        cap = cv2.VideoCapture(f"assets/{workout}.mp4") # VideoCapture(0) to use the live camera
        detector = pm.poseDetector()
        pTime = 0
        self.reps = 0
        repDrop = False
        neededAngles = data.fetchAngles(workout)

        if invert:  # We reverse the rep counting system depending on whether it is for example a squat or a pull-up
            # TODO Make more than two types of reward system and refactor them on their own file
            # TODO they would return a lambda function which would calculate the progression
            def calculate_progress(angle, angleMin, angleMax):
                """
                ...
                """
                angle = max(angleMin, min(angle, angleMax))
                progression = round(((angle - angleMax) / (angleMin - angleMax)) * 105)
                return progression
        else:
            def calculate_progress(angle, angle_min, angle_max):
                """
                ...
                """
                angle = max(angle_max, min(angle, angle_min))
                progression = round(((angle - angle_min) / (angle_max - angle_min)) * 100)
                return progression
            
        while self.reps < reps:
            success, img = cap.read()

            if success:
                img = detector.findPose(img, False)
                img = cv2.resize(img, (1024, 576))
                lmList = detector.findPosition(img, False)

                if len(lmList) != 0:
                    pose = self.poseHandler(img, detector, neededAngles)
                    expectations = data.lookup(workout, pose)
                    percentage = calculate_progress(*expectations[0])
                    if percentage >= 100 and repDrop == True:  # We also add a tolerance...
                        self.reps += 1
                        repDrop = False
                    elif percentage == 0:
                        repDrop = True

                    print(f"{percentage}% | Répétition : {self.reps}")

                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv2.putText(img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
                cv2.putText(img, f"{title}: {self.reps}", (800, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                cv2.imshow("bpump-cam", img)
                cv2.waitKey(1)
            else:
                cap.release()
                cv2.destroyAllWindows()
        return reps

    def poseHandler(self, img, detector, joint_names):
        """
        Manipulates the detected pose and returns a PoseType object

        :param img: The input image
        :param detector: The type of detector
        :param joint_names: The list of joints
        :return: The PoseType object representing the detected pose
        """
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