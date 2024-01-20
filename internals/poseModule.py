import cv2
import mediapipe as mp
import math

class poseDetector() :
    
    def __init__(self, mode=False, complexity=1, smooth_landmarks=True, enable_segmentation=False, smooth_segmentation=True, detectionCon=0.5, trackCon=0.5):
        """
        Initializing the class with specific parameters for model configuration and detection

        :param mode: Pose model detection mode (defaults to False)
        :param complexity: Complexity level of the pose model (default to 1)
        :param smooth_landmarks: Enabling or disabling landmark smoothing (defaults to True)
        :param enable_segmentation: Enable or disable segmentation (defaults to False)
        :param smooth_segmentation: Enabling or disabling segmentation smoothing (defaults to True)
        :param detectionCon: Confidence threshold for detection (defaults to 0.5)
        :param trackCon: Confidence threshold for tracking (defaults to 0.5)
        """
        self.mode = mode 
        self.complexity = complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth_landmarks, self.enable_segmentation, self.smooth_segmentation, self.detectionCon, self.trackCon)
        
    def findPose(self, img, draw=True):
        """
        Uses the pose model to detect pose in an image

        :param img: The image in which to detect the pose
        :param draw: Boolean indicating whether landmarks and connections should be drawn on the image (defaults to True)
        :return: The image with the landmarks and connections drawn
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
                
        return img
    
    def findPosition(self, img, draw=True):
        """
        Extracts and returns the list of positions of the detected landmarks

        :param img: The image from which to extract the positions of the landmarks
        :param draw: Boolean indicating whether landmarks should be drawn on the image (default to True)
        :return: A list containing the positions of landmarks
        """
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        return self.lmList
        
    def findAngle(self, img, p1, p2, p3, draw=True):
        """
        Calculates the angle formed by three specified points

        :param img: The image on which to draw the angle
        :param p1, p2, p3: Landmark indices to calculate the angle (https://lc.cx/PLZ6m7)
        :param draw: Boolean indicating whether the angle should be drawn on the image (defaults to True)
        :return: The calculated angle in degrees
        """
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
            if angle > 180:
                angle = 360 - angle
        elif angle > 180:
            angle = 360 - angle

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)  
            cv2.circle(img, (x1, y1), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        return angle