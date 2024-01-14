import json

with open("./data/workouts.json", "r") as read_file:
    data = json.load(read_file)
    print(data['workouts'])


def lookup(exercice, pose):
    """
    Très simplement, on vient chercher un exercice pour trouver les angles qu'il faut regarder, les valeurs mins et max
    :param exercice: Le nom
    :param pose: On passe la position pour renvoyer une valeur d'angle
    :return: Un array avec le lookup nécéssaire de chaque côté
    """
    parsed = data['workouts'][exercice]
    return [
        [
            getattr(pose, parsed['left']['angle']),
            parsed['left']['minAngle'],
            parsed['left']['maxAngle']
        ],
        [
            getattr(pose, parsed['right']['angle']),
            parsed['right']['minAngle'],
            parsed['right']['maxAngle']
        ]

    ]
