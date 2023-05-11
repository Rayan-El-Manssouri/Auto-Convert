import fitz

# Ouvrir le fichier PDF en mode lecture
with fitz.open("example.pdf") as pdf:
    # Ensemble pour stocker les mots déjà traités
    processed_words = set()

    # Variable pour compter le nombre de mots contenant au moins un "f"
    count = 0

    # Parcourir chaque page du fichier PDF
    for page in pdf:
        # Parcourir chaque mot de la page
        for word in page.get_text_words():
            # Convertir le tuple en dictionnaire
            word_dict = {
                "x0": word[0],
                "y0": word[1],
                "x1": word[2],
                "y1": word[3],
                "text": word[4],
                "size": word[5],
                "font": word[6],
                "color": word[7],
            }

            # Vérifier si le mot a déjà été traité
            if word_dict["text"] in processed_words:
                continue  # Passer au mot suivant si déjà traité

            # Ajouter le mot à l'ensemble des mots traités
            processed_words.add(word_dict["text"])

            # Vérifier si le mot contient au moins un "f"
            if "f" in word_dict["text"]:
                count += 1
                print(
                    "Position du caractère f :",
                    word_dict["x0"],
                )

    print("Nombre total de mots contenant au moins un f :", count)
