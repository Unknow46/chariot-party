# coding: utf-8

from interface import *
from random import randint
from datetime import *

# Echelon 1

# plateau = [1, 1, 3, 3, 3, 2, 1, 3, 3, 1, 2, 3, 3, 3, 3, 1, 3, 3, 3, 3]
plateau = []
# gold = 24
players = []
# players =[{'position':3, 'charbon':4, 'or':0},
#          {'position':8, 'charbon':10, 'or':0},
#          {'position':16, 'charbon':3, 'or':1},
#          {'position':7, 'charbon':0, 'or':0}]


# creePlateau(plateau)
# creeJoueurs(players, plateau)
# placeOr(gold, plateau)

#########################################################################################
# Echelon 2
"""
nbJoueurs = int(input("Nombre de Joeurs ?"))
while nbJoueurs > 4 or nbJoueurs < 0 :
    nbJoueurs=int(input("Nombre incorecte, saisir a nouveau : "))

nbTours = int(input("Nombre de Tours ?"))
while nbTours < 0 :
    nbTours=int(input("Nombre incorrecte de tour, saisir a nouveau :"))

nbCases = int(input("Nombre de Cases ?"))
while nbCases % 4 != 0:
    nbCases = int(input("Le nombre de case est incorrecte, saisir à nouveau : "))

boucle = 0

while boucle < nbJoueurs:
    players.append({'position': 0, 'charbon': 0, 'or': 0})
    boucle = boucle+1

boucle2 =0

while boucle2 < nbCases:
    plateau.append(randint(1, 3))
    boucle2 = boucle2+1

gold = randint(0, nbCases)

creePlateau(plateau)
creeJoueurs(players, plateau)
placeOr(gold, plateau)
"""
########################################################################################

# Echelon 3

nbJoueurs = 0
nbTours = 0
nbCases = 0
gold = 0
nbFaces = 6


def safe_input(text, in_type, validation=lambda x: True, non_validate_value=None):
    """

        :param text: Texte à afficher au terminal pour la saisie utilisateur
        :param in_type: Le type de la valeur attendue (int, float, str...)
        :param validation: Fonction prennant en paramètre une valeure du type in_type et renvoyant True ou False
            si la valeur respecte les conditions attendues
        :param non_validate_value: Valeur ne respectant pas la condition
            (pour traiter le cas initial où nous n'avons rien)
        :return: Valeur saisie par l'utilisateur
    """
    res = None
    if in_type in [dict, list, tuple]:
        in_type = eval
    while not res or not validation(res or non_validate_value):
        try:
            res = in_type(input(text))
        except:
            print("Merci de saisir une valeur correcte.")
    return res


def configuration():
    global nbCases, nbJoueurs, nbTours

    nbJoueurs = safe_input("Veuillez saisir un nombre entre 1 et 4 inclus: ", int, lambda x: x in range(1, 5))
    nbTours = safe_input("Veuillez saisir un nombre de tour: ", int, lambda x: x > 0)
    nbCases = safe_input("Veuillez saisir un nombre de cases (multiple de 4 et > à 0): ", int,
                         lambda x: x % 4 == 0 and x >= 4)

    for i in range(nbCases):
        plateau.append(randint(1, 3))


def initialisationJoueurs(nbJoueurs):
    for i in range(nbJoueurs):
        players.append({'id': i, 'position': 0, 'charbon': 5, 'or': 0})
    creeJoueurs(players, plateau)


def positionGold(nbCases):
    global gold
    gold = randint(0, nbCases)


def initialisation():
    configuration()
    creePlateau(plateau)
    initialisationJoueurs(nbJoueurs)
    positionGold(nbCases)
    placeOr(gold, plateau)


def lanceDe(nbFaces):
    return randint(1, nbFaces)


def acheteLingot(player):
    if player["position"] == gold and player["charbon"] >= 10:
        print("Le joueur %s est sur une case avec de l'or, il a %s charbons en stock, souhaitez-vous le prendre pour "
              "10 charbons ?" % (player['id'], player['charbon']))
        took_gold = safe_input(
            "Prendre l'or ? (oui/non): ", str, lambda x: x.lower() in ['oui', 'non'],
            non_validate_value='').lower()
        if took_gold == "oui":
            player["charbon"] -= 10
            player["or"] += 1

            positionGold(nbCases)
            placeOr(gold, plateau)


def effetCase(players, plateau):
    if plateau[players["position"]] == 1:
        players["charbon"] += 3

    if plateau[players["position"]] == 2:
        if int(players["charbon"]) - 3 > 0:
            players["charbon"] -= 3


def deplaceJoueur(players, lancer_de, plateau):

    for i in range(lancer_de):
        players["position"] = (players["position"] + 1) % len(plateau)
        bougeJoueur(players, plateau)
        acheteLingot(players)
    effetCase(players, plateau)

def tourJoueur(players, plateau):
    deplaceJoueur(players, lanceDe(6), plateau)


def tourDeJeu(players):
    for player in players:
        tourJoueur(player, plateau)


def partie(nbTours, players):
    for i in range(nbTours):
        tourDeJeu(players)


# initialisation()
# partie(nbTours, players)


##########################################################################

# Echelon 4


def compJoueurs(player1, player2):
    # On compare d'abord le nombre d'or
    if player1["or"] > player2["or"]:
        return 1
    elif player1["or"] < player2["or"]:
        return -1

    # Si égalité dans l'or on compare les charbons
    if player1["charbon"] > player2["charbon"]:
        return 1
    if player1["charbon"] < player2["charbon"]:
        return -1

    return 0


def winner(players):
    flag = True
    while flag:
        flag = False
        for i in range(len(players) - 1):
            if compJoueurs(players[i], players[i + 1]) == -1:
                tmp = players[i + 1]
                players[i + 1] = players[i]
                players[i] = tmp
                flag = True

    return players


def sauvegardeResultats(players):
    today = datetime.today()
    name = 'chariot-party-%s.txt' % ('-'.join(map(str, [
        today.day, today.month, today.year,
        today.hour, today.minute
    ])))  # Peut être remplacer par: name = 'chariot-party-%s.txt' % (today.strftime('%d-%m-%Y-%H-%M')
    with open(name, 'w', encoding='utf-8') as f:
        f.write(players)


def afficheClassement(players):
    classement = winner(players)

    affichage = '\n'.join(["Numéro %s avec %s lingot(s) d'or et %s charbon(s)" % (
        player['id'], player['or'], player['charbon']) for player in classement])

    sauvegardeResultats(affichage)


# afficheClassement(players)


if __name__ == '__main__':
    initialisation()
    partie(nbTours, players)
    afficheClassement(players)
