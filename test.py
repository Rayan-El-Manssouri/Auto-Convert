import fitz

# Ouvrir le fichier PDF en mode lecture
with fitz.open("example.pdf") as pdf:
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
            # Parcourir chaque caractère du mot
            for char_info in word_dict["text"]:
                # Récupérer la couleur du caractère en tant que valeur décimale
                char_color_decimal = int(word_dict["color"])
                # Convertir la valeur décimale en hexadécimal et ajouter des zéros à gauche si nécessaire
                char_color_hex = hex(char_color_decimal)[2:].zfill(6)
                # Extraire les valeurs des composantes rouge, vert et bleu de l'hexadécimal
                r = int(char_color_hex[0:2], 16)
                g = int(char_color_hex[2:4], 16)
                b = int(char_color_hex[4:6], 16)
                # Afficher la couleur RGB correspondante
                print(
                    "Couleur du caractère ", char_info, " : (", r, ",", g, ",", b, ")"
                )
