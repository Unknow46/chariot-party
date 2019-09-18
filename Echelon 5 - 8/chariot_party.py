# coding: utf-8

from interface_objet import *
from joueur import Joueur
from case import Case
from random import randint
from datetime import *

plateau = []
players = []

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
    nbCases = safe_input("Veuillez saisir un nombre de cases (multiple de 4 et > à 0): ", int, lambda x: x % 4 == 0 and x >= 4)

    for i in range(nbCases):
        plateau.append(Case(randint(1, 3)))


def initialisationJoueurs(nbJoueurs):
    for i in range(nbJoueurs):
        players.append(Joueur(i))
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
    if player.position == gold and player.charbon >= 10:
        print("Le joueur %s est sur une case avec de l'or, il a %s charbons en stock, souhaitez-vous le prendre pour "
              "10 charbons ?" % (player.id, player.charbon))
        took_gold = safe_input(
            "Prendre l'or ? (oui/non): ", str, lambda x: x.lower() in ['oui', 'non'],
            non_validate_value='').lower()
        if took_gold == "oui":
            player.charbon -= 10
            player.n_or += 1

            positionGold(nbCases)
            placeOr(gold, plateau)


def deplaceJoueur(player, lancer_de, plateau):
    player.deplacer(lancer_de, plateau)
    bougeJoueur(player, plateau)
    plateau[player.position].effet(player)
    acheteLingot(player)


def tourJoueur(players, plateau):
    deplaceJoueur(players, lanceDe(6), plateau)


def tourDeJeu(players):
    first_player = 0
    boucle = 0

    while boucle < len(players):
        tourJoueur(players[first_player], plateau)

        if first_player + 1 > len(players):
            first_player = 0

        if boucle > len(players):
            boucle = 0

        first_player += 1
        boucle += + 1


def partie(nbTours, players):
    boucle = 0
    while boucle < nbTours:
        tourDeJeu(players)
        boucle += 1

def winner(players):
    flag = True
    while flag:
        flag = False
        for i in range(len(players) - 1):
            if players[i] < players[i + 1]:
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
            player.id, player.n_or, player.charbon) for player in classement])

    sauvegardeResultats(affichage)


if __name__ == '__main__':
    initialisation()
    partie(nbTours, players)
    afficheClassement(players)
