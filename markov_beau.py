import random
import os
import sys
import readchar

def print_bar(current, total):
    percent = round(current/total * 50)
    print("\033[F [", end="")
    for i in range(percent):
        print("#", end="")
    for i in range(50 - percent):
        print(" ", end="")

    print(f"] {percent * 2} %")

def select_file():
    print("Sélection du fichier d'entrée (utiliser (q et d) ou (flèches <- ->) pour se déplacer)\n")

    selection = 0

    dirs = os.listdir()
    maxi = len(dirs)
    print("\033[F", end="")
    while True:
        print("\033[1m", end="")
        r = repr(readchar.readkey())
        if r == "'q'" or r == "'\\x1b[D'":
            selection = (selection - 1) % maxi
        elif r == "'\\n'":
            print()
            return dirs[selection]
        elif r == "'d'" or r == "'\\x1b[C'":
            selection = (selection + 1) % maxi
        for f in dirs:
            if dirs.index(f) == selection:
                print(" \033[31m[", f, "]\033[0m\033[1m", sep="", end="")
            else:
                print("", f, end = "")
        os.system("clear")
        print("\033[0m")
        sys.stdout.flush()


def main():
    filename = select_file()
    print()
    file = open(filename, "r")
    content = file.read()
    file.close()
    content = content.split() # on sépare la liste de mots par les retours a la ligne

    if (len(content) > 20000):
        max_ = round(len(content) / 20000) # pour les listes trop grandes
    else:
        max_ = 1
    mots = [] # la liste de mots
    lettres = [] # la liste des lettres
    debuts_mot = [] # la liste de lettres qui débutent les mots
    
    nb = int(input("nombre de mots à générer : "))
    longueur_analyse = input("longeure des chaines de caractères à prendre en compte (rien pour 2) : ") # la longueur des chaines analysées
    if longueur_analyse == "":
        longueur_analyse = 2
    else:
        longueur_analyse = int(longueur_analyse)

    # on prend un nombre au hasard
    # comme ça on ne prend pas a chaques fois le premier mot de départ 
    # on analyse donc pas les mêmes mots a chaques fois
    count = random.randint(0, 100)

    print("Lecture du fichier ...\n")
    for i in content:
        if count % max_ == 0:
            # On exclue un certain nombre de mots indésirables et d'erreures de la liste de mots
            if " " in i or (len(i) > 0 and i[0].capitalize() == i[0]) or len(i) < longueur_analyse:
                pass
            else:
                index = content.index(i)
                mots.append(content[index] + " ")
                print_bar(index, len(content))
        count += 1

    for i in mots:
        debuts_mot.append( i[:longueur_analyse] )
        for j in i:
            if j not in lettres:
                lettres.append(j)

    del content # on as vraiment besoin de se séparer de la grosse liste pour les fichiers volumineux
    

    # Pour la chaine de markov, on regarde les n premières lettres et on regarde celle qui viens
    prems2 = {}

    print("Analyse de la liste de mots...\n")
    
    for i in mots:
        if len(i) == 1 or len(i) == 2:
            continue
        for x in range(len(i) - longueur_analyse):
            t = i[x : x + longueur_analyse]
            suiv = i[x + longueur_analyse]
            if t not in prems2:
                prems2[t] = [0 for i in range(len(lettres))]
            prems2[t][lettres.index(suiv)] += 1
            print_bar(mots.index(i), len(mots))
            

    for i in prems2:
        s = sum(prems2[i])
        for x in range(len(prems2[i])):
            prems2[i][x] = prems2[i][x] / s

    generated_words = []

    print("Génération des mots...\n")
    for i in range(nb):
        premier_bout = random.choice(debuts_mot)

        mot = premier_bout

        c = random.random()
        s = 0
        l = ""

        while l != " ":
            for proba in prems2[premier_bout]:
                s += proba
                if c <= s:
                    l = lettres[prems2[premier_bout].index(proba)]
                    mot += l
                    premier_bout = premier_bout[1:] + l
                    c = random.random()
                    s = 0
                    break
        if mot not in generated_words:
            generated_words.append(mot)
            print_bar(i, nb)
    
    full = ""
    for i in generated_words:
        full += i + "\n"
    
    file = open(f"out_{filename}", "w")
    file.write(full)
    file.close()
    print(f"fichier écrit : out_{filename}")
    print(f"Nombre de mots générés : {len(generated_words)}")
    
if __name__ == "__main__":
    main()