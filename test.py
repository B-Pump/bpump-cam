from main import Exercices
exercices = Exercices()


response = str(input(f"""{"="*100}
    Quelles exercice veux-tu faire ?
        1 - Pullup
{"="*100}

    Réponse: """))

if response == "1":
    print(exercices.start("squat", 3))
    print(exercices.start("pullup", 2))
