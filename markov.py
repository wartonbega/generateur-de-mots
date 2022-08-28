import random


def main():
    filename = "fra_wordlist.txt"
    file = open(filename, "r")
    content = file.read()
    file.close()
    content = content.split() # on sépare la liste de mots par les retours a la ligne


    if (len(content) > 20000):
        max_ = round(len(content) / 20000) # pour les listes trop grandes
    else:
        max_ = 1

    mots = [] # la liste de mots
    
    # Le nombre de mots a générer
    nb = 100
    
    # La longueur des chaines de caractère à analyser
    longueur_analyse = 3

    # on prend un nombre au hasard
    # comme ça on ne prend pas a chaques fois le premier mot de départ 
    # on analyse donc pas les mêmes mots a chaques fois
    count = random.randint(0, 100)

    for i in range(len(content)):
        if i % max_ == 0:
            # On exclue un certain nombre de mots indésirables et d'erreures de la liste de mots
            if " " in content[i] or (len(content[i]) > 0 and content[i][0].capitalize() == content[i][0]) or len(content[i]) < longueur_analyse:
                pass
            else:
                mots.append(content[i] + " ")


    del content # on as vraiment besoin de se séparer de la grosse liste pour les fichiers volumineux
    

    lettres = [] # la liste des lettres
    debuts_mot = [] # la liste de lettres qui débutent les mots
    for i in mots:

        # Pour pouvoir générer des mots cohérent, on ne prend que des débuts de mots déja existants
        # Par exemple pour ne pas commencer par 'zh' (improbable en français)
        debuts_mot.append( i[:longueur_analyse] )
        for j in i:
            if j not in lettres:
                # On se crée notre propre liste de caractères pour ne générer des mots
                # uniquement avec des caractères existants dans la liste d'entré
                lettres.append(j)

    # Pour la chaine de markov, on regarde les n premières lettres et on regarde celle qui viens
    prems2 = {}
    for i in range(len(mots)):
        if len(mots[i]) == 1 or len(mots[i]) == 2:
            continue
        for x in range(len(mots[i]) - longueur_analyse):
            # t est les n premières lettres analysées
            t = mots[i][x : x + longueur_analyse]

            # et suiv la lettres suivante
            suiv = mots[i][x + longueur_analyse]
            if t not in prems2:
                # Si on ne connais pas encore la suite de caractère t 
                # on lui crée une place dans le dictionnaire et on initialise 
                # son compte de lettre
                prems2[t] = [0 for _ in range(len(lettres))]
            prems2[t][lettres.index(suiv)] += 1

    # On met toute les sommes en proba
    for i in prems2:
        s = sum(prems2[i])
        for x in range(len(prems2[i])):
            prems2[i][x] = prems2[i][x] / s

    generated_words = [] # La liste des mots déjà générés

    for i in range(nb):
        premier_bout = random.choice(debuts_mot)

        mot = premier_bout

        c = random.random()
        s = 0 # La somme des probabilités des lettres 'suivantes'
        l = ""

        while l != " ":
            for proba in prems2[premier_bout]:
                s += proba
                if c <= s:
                    l = lettres[prems2[premier_bout].index(proba)]
                    mot += l

                    # La première lettre de la génération est abandonnée
                    # Mais on rajoute la nouvelle lettre générée
                    premier_bout = premier_bout[1:] + l
                    
                    # On réinitialise tout 
                    c = random.random()  
                    s = 0
                    break 

        # On ne veux pas générer deux fois le même mot
        if mot not in generated_words:
            print(mot)
    
if __name__ == "__main__":
    main()