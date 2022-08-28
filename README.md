# generateur-de-mots
Un générateur de mots basé sur des chaines de markov

Deux programmes possibles : `markov.py` et `markov_beau.py`.

Le premier vas prendre en entrée la liste de mots français. Il est simple, juste l'algorithme.

Le second vas demander un certain nombre de paramètre avant de lancer la génération, et donne une avancée globale. Il génère un fichier de sortie contenant les mots générés.

## Prérequis
`markov.py` demande uniquement d'avoir dans le même répertoir `fra_wordlist.txt`.

`markov_beau.py` necessite entre autre d'avoir au moins un fichier d'entrée dans le même repertoire, et necessite la bibiothèque python `readchar`.
Pour l'installer : `pip install readchar` ou `pip3 install readchar` ou `python3.X -m pip install readchar`.

