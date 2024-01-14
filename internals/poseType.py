class PoseType:
    def __init__(self, joint_names, angles):
        for name, angle in zip(joint_names, angles):
            setattr(self, name, angle)
