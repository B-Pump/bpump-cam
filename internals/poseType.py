class PoseType:
    
    def __init__(self, joint_names, angles):
        """
        Méthode d'initialisation de la classe

        :param joint_names: Une liste de noms de jointures
        :param angles: Une liste d'angles correspondants aux jointures
        """
        for name, angle in zip(joint_names, angles):
            setattr(self, name, angle)