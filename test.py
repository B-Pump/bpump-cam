from main import Exercices
exercices = Exercices()


response = str(input(f"""{"="*100}
    Quelles exercice veux-tu faire ?
        1 - Pullup
        2 - curl
        3 - pushup
        4 - situp
        5 - squat
{"="*100}

    Réponse: """))

if response == "1":
    exercices.start("pullup")
elif response == "2":
    exercices.start("curl")
elif response == "3":
    exercices.start("pushup")
elif response == "4":  
    exercices.start("situp")
elif response == "5":
    exercices.start("squat")
