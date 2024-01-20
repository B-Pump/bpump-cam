class PoseType:
    
    def __init__(self, joint_names, angles):
        """
        Class initialization method

        :param joint_names: A list of join names
        :param angles: A list of angles corresponding to the joins
        """
        for name, angle in zip(joint_names, angles):
            setattr(self, name, angle)