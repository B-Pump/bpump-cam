import json

with open("./data/workouts.json", "r") as read_file:
    data = json.load(read_file)


def fetchSugar(exercice):
    parsed = data['workouts'][exercice]
    return parsed['sugar']['title']


def fetchInvert(exercice):
    parsed = data['workouts'][exercice]
    if 'invertReward' not in parsed['sugar']:
        return False
    return True


def fetchAngles(exercice):
    parsed = data['workouts'][exercice]
    angles = []
    for attribute in parsed:
        if 'angle' in parsed[attribute]:
            angles.append(parsed[attribute]['angle'])
    print(angles)
    return angles


def lookup(exercice, pose):
    """
    Très simplement, on vient chercher un exercice pour trouver les angles qu'il faut regarder, les valeurs mins et max
    :param exercice: Le nom
    :param pose: On passe la position pour renvoyer une valeur d'angle
    :return: Un array avec le lookup nécéssaire de chaque côté
    """
    parsed = data['workouts'][exercice]
    if parsed == None:
        raise FileNotFoundError
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
