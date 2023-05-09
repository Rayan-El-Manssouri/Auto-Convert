<p align="center">
  <a href="https://github.com/Rayan-El-Manssouri/Auto-Convert#readme">
    <img src="./assets/AutoConvertLogo.png" alt="Auto Convert logo" style="width: 230px;" >
  </a>
</p>

<h3 align="center">Auto Convert</h3>
<p align="center"><i>Transformez vos PDF en composants React grâce à ce script Python innovant !</i></p>

___
![Top language (GitHub)](https://img.shields.io/github/languages/top/Rayan-El-Manssouri/Auto-Convert)


Auto Convert est un script Python qui permet de convertir un fichier PDF en un composant React optimisé. Cette conversion peut être utile pour l'intégration de documents PDF dans des projets React.

## Prérequis

Avant de pouvoir utiliser Auto Convert, vous devez avoir les éléments suivants installés sur votre système :

- Python
- pip

## Installation

Pour installer Auto Convert, vous pouvez suivre les étapes suivantes :

1. Clonez le référentiel GitHub vers votre ordinateur

```white
git clone https://github.com/Rayan-El-Manssouri/Auto-Convert
```

2. Accédez au répertoire du projet

```white
cd auto-convert
```

3. Installez les dépendances

```white
  pip install -r requirements.txt
```

## Utilisation

Pour utiliser Auto Convert, vous pouvez suivre les étapes suivantes :

1. Placez le fichier PDF que vous souhaitez convertir à la racine du projet.

2. Exécutez le script Python en fonction de votre système d'exploitation.


Windows

```white
  python main.py
```

Linux

```white
  python3 main.py
```

3. Le composant React optimisé sera généré dans le fichier défini du `config.ini`.

## Arborescence du projet

- `/` : dossier racine contenant le fichier principal.
- `/assets` : dossier contenant toutes les images utilisées dans le projet, sauf les images du PDF généré.
- `/generateReactComponent` : dossier contenant le composant React qui crée les variables pour le fichier JavaScript.
- `*/maths` : dossiers contenant tous les calculs mathématiques utilisés dans le projet.
- `*/config.init` : fichiers contenant les variables nécessaires à la configuration de la sortie (PDF, JSON, fichier de sortie).


## Configuration

Le fichier `config.ini` est utilisé pour stocker des variables de configuration pour notre application. Il contient plusieurs sections avec des variables spécifiques pour chaque section.

Une fois que vous avez configuré les variables dans le fichier `config.ini`, vous devez enregistrer le fichier pour que les modifications soient prises en compte.

# License

Veuillez noter que le fichier [MIT License](https://github.com/Rayan-El-Manssouri/Auto-Convert/blob/master/LICENSE.) contient les termes et conditions de la licence pour l'utilisation de ce logiciel.
