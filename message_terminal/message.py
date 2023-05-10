# Importez la bibliothèque colorama
from colorama import init, Fore, Back, Style
import time

# Initialisez la bibliothèque colorama
init()


def color_text_terminal(message, text_color, transition_speed):
    # Initialisez une variable pour stocker le message à afficher
    output = ""

    # Parcourez le message caractère par caractère et ajoutez chaque caractère au message de sortie avec une pause entre chaque caractère
    for char in message:
        output += char
        color = getattr(Fore, text_color.upper())
        print(color + output + Style.RESET_ALL, end="\r", flush=True)
        time.sleep(transition_speed)

    # Ajoutez une pause avant d'afficher le message suivant
    time.sleep(transition_speed)

    # Affichez le message complet avec les couleurs définies
    color = getattr(Fore, text_color.upper())
    print(color + message + Style.RESET_ALL)
