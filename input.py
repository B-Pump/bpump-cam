from main import Exercices

exercices = Exercices()

reponse = str(input(f"""{"="*100}
    Quelles exercice veux-tu faire ?
        1 - Pullup
        2 - curl
        3 - pushup
        4 - situp
        5 - squat
{"="*100}

    Réponse: """))

if reponse == "1":
    exercices.start("pullup", 10)
elif reponse == "2": 
    exercices.start("curl", 10)
elif reponse == "3":
    exercices.start("pushup", 10)
elif reponse == "4":
    exercices.start("situp", 10)
elif reponse == "5":
    exercices.start("squat", 10)