import cv2
import mediapipe as mp
import math

class poseDetector() :
    
    def __init__(self, mode=False, complexity=1, smooth_landmarks=True, enable_segmentation=False, smooth_segmentation=True, detectionCon=0.5, trackCon=0.5):
        """
        Initialisation de la classe avec des paramètres spécifiques pour la configuration du modèle et la détection

        :param mode: Mode de détection du modèle pose (par défaut sur False)
        :param complexity: Niveau de complexité du modèle pose (par défaut à 1)
        :param smooth_landmarks: Activation ou désactivation du lissage des landmarks (par défaut sur True)
        :param enable_segmentation: Activation ou désactivation de la segmentation (par défaut sur False)
        :param smooth_segmentation: Activation ou désactivation du lissage de la segmentation (par défaut sur True)
        :param detectionCon: Seuil de confiance pour la détection (par défaut à 0.5)
        :param trackCon: Seuil de confiance pour le suivi (par défaut à 0.5)
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
        Utilise le modèle pose pour détecter la pose dans une image

        :param img: L'image dans laquelle détecter la pose
        :param draw: Booléen indiquant si les landmarks et les connexions doivent être dessinés sur l'image (par défaut sur True)
        :return: L'image avec les landmarks et les connexions dessinés
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
                
        return img
    
    def findPosition(self, img, draw=True):
        """
        Extrait et renvoie la liste des positions des landmarks détectés

        :param img: L'image à partir de laquelle extraire les positions des landmarks
        :param draw: Booléen indiquant si les landmarks doivent être dessinés sur l'image (par défaut sur True)
        :return: Une liste contenant les positions des landmarks
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
        Calcule l'angle formé par trois points spécifiés

        :param img: L'image sur laquelle dessiner l'angle
        :param p1, p2, p3: Indices des landmarks pour calculer l'angle (https://lc.cx/PLZ6m7)
        :param draw: Booléen indiquant si l'angle doit être dessiné sur l'image (par défaut sur True)
        :return: L'angle calculé en degrés
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