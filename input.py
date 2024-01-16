from main import Exercices

exercices = Exercices()

reponse = input("\nQuelles exercice veux-tu faire ?\n1 - Pullup\n2 - curl\n3 - pushup\n4 - situp\n5 - squat\n\nRéponse: ")

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