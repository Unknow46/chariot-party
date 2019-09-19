# coding: utf-8
from interface_objet import *
from joueur import Joueur
from fabrique_case import FabriqueCase
from random import randint
import random
from datetime import *


def lanceDe(de):
    return randint(1, de)


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


class Plateau(FabriqueCase):

    def __init__(self, plateau, players, nbJoueurs, nbCases, gold):
        self.plateau = plateau
        self.players = players
        self.nbJoueurs = nbJoueurs
        self.nbCases = nbCases
        self.gold = gold

        self.configuration()
        creePlateau(self.plateau)
        self.initialisationJoueurs()
        self.positionGold()
        placeOr(self.gold, self.plateau)

    def configuration(self):
        self.nbJoueurs = safe_input("Veuillez saisir un nombre entre 1 et 4 inclus: ", int,
                                         lambda x: x in range(1, 5))
        self.nbTours = safe_input("Veuillez saisir un nombre de tour: ", int, lambda x: x > 0)
        self.nbCases = safe_input("Veuillez saisir un nombre de cases (multiple de 4 et > à 0): ", int,
                                       lambda x: x % 4 == 0 and x >= 4)

        fabrique = FabriqueCase()
        for i in range(self.nbCases):

            case = []
            case.extend([1 for i in range(25)])  # 25% de vert
            case.extend([2 for i in range(20)])  # 20% de rouge
            case.extend([3 for i in range(50)])  # 50% de bleu
            case.extend([4 for i in range(5)])  # 5 % de jaune

            new_case = random.choice(case)

            self.plateau.append(fabrique.create(new_case))

    def initialisationJoueurs(self):
        for i in range(self.nbJoueurs):
            self.players.append(Joueur(i))
        creeJoueurs(self.players, self.plateau)

    def positionGold(self):
        self.gold = randint(0, self.nbCases)

    def acheteLingot(self, player):
        if player.position == self.gold and player.charbon >= 10:
            print(
                "Le joueur %s est sur une case avec de l'or, il a %s charbons en stock, souhaitez-vous le prendre pour "
                "10 charbons ?" % (player.id, player.charbon))
            took_gold = safe_input(
                "Prendre l'or ? (oui/non): ", str, lambda x: x.lower() in ['oui', 'non'],
                non_validate_value='').lower()
            if took_gold == "oui":
                player.charbon -= 10
                player.n_or += 1

                self.positionGold()
                placeOr(self.gold, self.plateau)

    def deplaceJoueur(self, player, lancer_de):
        player.deplacer(lancer_de, self)
        self.plateau[player.position].effet(player)

    def tourDeJeu(self):
        for player in self.players:
            self.deplaceJoueur(player, lanceDe(6))

    def partie(self):
        for i in range(self.nbTours):
            self.tourDeJeu()

    def winner(self):
        flag = True
        while flag:
            flag = False
            for i in range(len(self.players) - 1):
                if self.players[i] < self.players[i + 1]:
                    tmp = self.players[i + 1]
                    self.players[i + 1] = self.players[i]
                    self.players[i] = tmp
                    flag = True
        # Si players devient une liste avec beaucoup de donnée faire self.players.sort() au lieu de la boucle précédente
        return self.players

    def sauvegardeResultats(self, players):
        today = datetime.today()
        name = 'chariot-party-%s.txt' % ('-'.join(map(str, [
            today.day, today.month, today.year,
            today.hour, today.minute
        ])))  # Peut être remplacer par: name = 'chariot-party-%s.txt' % (today.strftime('%d-%m-%Y-%H-%M')
        with open(name, 'w', encoding='utf-8') as f:
            f.write(players)

    def afficheClassement(self):
        classement = self.winner()

        affichage = '\n'.join(["Numéro %s avec %s lingot(s) d'or et %s charbon(s)" % (
            player.id, player.n_or, player.charbon) for player in classement])

        self.sauvegardeResultats(affichage)

    def play(self):
        self.partie()
        self.afficheClassement()
