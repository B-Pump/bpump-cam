class PoseType:
    def __init__(self, angles, legangles):
        self.angleLeftArm, self.angleLeftUpperLeg, self.angleLowerLeg, \
            self.angleRightArm, self.angleRightUpperLeg, self.angleRightLowerLeg = angles
        (self.angleLeftArm, self.angleLeftHip, self.angleLeftLeg, self.angleLeftFoot,
         self.angleRightArm, self.angleRightHip, self.angleRightLeg, self.angleRightFoot) = legangles
