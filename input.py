from main import Exercices

exercices = Exercices()

user_input = input("Quel exercice veux-tu faire et combien de répétitions ?\n1 - Tractions\n2 - Curls\n3 - Pompes\n4 - Sit-up\n5 - Squats\n\nFormat : <exo> <reps>\n\nRéponse : ")

user_input_list = user_input.split()
if len(user_input_list) == 2:
    exo, reps = user_input_list
    reps = int(reps)

    if exo == "1":
        exercices.start("pullup", reps)
    elif exo == "2":
        exercices.start("curl", reps)
    elif exo == "3":
        exercices.start("pushup", reps)
    elif exo == "4":
        exercices.start("situp", reps)
    elif exo == "5":
        exercices.start("squat", reps)