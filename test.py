from Exo import Exercices
exercices = Exercices()


response = str(input(f"""{"="*100}
    Quelles exercice veux-tu faire ?
        1 - Pull up 
{"="*100}

    Réponse: """))

if response == "1":
    exercices.pull_Up()