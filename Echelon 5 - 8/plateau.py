# coding: utf-8
from interface_objet import *
from joueur import Joueur
from fabrique_case import FabriqueCase
from random import randint
import random
from datetime import *


def lanceDe(de):
    """
    :param de: nombre de face du dé
    :return:  renvoie une des faces du dé
    """
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

    def verif_is_int(self, text):
        res = screen.numinput("Interaction", text)

        while res not in range(len(self.players)):
            res = screen.numinput("Interaction", text)

        return res

    def __init__(self):
        """
        Initialisation du plateau et appelle des fonctions pour son affichage
        (placement joueur, objet...)
        """
        self.plateau = []
        self.players = []
        self.nbJoueurs = 0
        self.nbCases = 0
        self.swap = 0
        self.gold = 0
        self.voleur = 0
        self.configuration()
        creePlateau(self.plateau)
        self.initialisationJoueurs()
        self.positionGold()
        self.positionSwap()
        self.positionVoleur()

    def configuration(self):
        """
        Demande à l'utilisateur de saisir les paramètres nécessaire à la création du plateau
        nombre de joueurs, de tour et de case.

        on appelle pare la suite la classe 'FabriqueCase' pour créer
        :return:
        """
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
        """
        Cette fonction permet de créer et d'ajouter les joueurs sur le plateau.
        :return:
        """
        for i in range(self.nbJoueurs):
            self.players.append(Joueur(i))
        creeJoueurs(self.players, self.plateau)

    def positionGold(self):
        """
        Cette fonction positionne aléatoirement un lingot d'or sur le plateau.
        :return:
        """
        self.gold = randint(0, self.nbCases)
        placeOr(self.gold, self.plateau)

    def positionSwap(self):
        """
        Cette fonction positionne de manière aléatoire la case 'swap' sur le plateau.
        :return:
        """
        self.swap = randint(0, self.nbCases)
        placeSwap(self.swap, self.plateau)

    def positionVoleur(self):
        """
        Cette fonction positionne aléatoirement la case 'voleur' sur le plateau.
        :return:
        """
        self.voleur = randint(0, self.nbCases)
        placeVoleur(self.voleur, self.plateau)

    def Swap(self, player):
        """
        Cette fonction permet de proposer à un joueur d'échanger son chariot avec un autre de son choix.
        :param player: Il s'agit du joueur s'arrétant sur la case swap.
        :return:
        """
        if player.position == self.swap:
            print("Le joueur %s est sur la case swap, il peut echanger son chariot avec un autre joueur souhaitez-vous "
                  "procéder à l'échange ?" % player.id)

            valide_swap = safe_input("Effectuer le changement de chariot ? (oui/non): ", str,
                                     lambda x: x.lower() in ["oui", "non"], non_validate_value='').lower()
            if valide_swap == "oui":
                for element in self.players:
                    print("Joueur %s avec %s charbon et %s or \n" % (element.id, element.charbon, element.n_or))

                joueur_choisis = self.verif_is_int("Entrer le numéro du joueur avec qui echanger votre chariot:")

                for player_selected in self.players:
                    if joueur_choisis == player_selected.id:
                        tempo_id = player_selected.id
                        player_selected.id = player.id
                        player.id = tempo_id

                self.positionSwap()

    def Voleur(self, player):
        """
        Cette fonction permet de proposer à un joueur de voler un lingot d'or au joueur de son choix.
        :param player: Il s'agit du joueur s'arrétant sur la case voleur.
        :return:
        """
        player_having_gold = 0
        if player.position == self.voleur:
            print("Le joueur %s est sur la case voleur, il peut voler un lingot d'or a un autre joueur "
                  "souhaitez-vous procéder au vol ?" % player.id)

            valide_vol = safe_input("Effectuer le vol ? (oui/non): ", str,
                                    lambda x: x.lower() in ["oui", "non"], non_validate_value='').lower()

            if valide_vol == "oui":
                for element in self.players:
                    if int(element.n_or) > 0:
                        player_having_gold += 1

                if player_having_gold > 0:
                    for element in self.players:
                        print("Joueur %s avec %s charbon et %s or \n" % (element.id, element.charbon, element.n_or))

                    joueur_choisis = self.verif_is_int("Entrer le numéro du joueur avec que vous souhaitez voler: ")

                    for player_selected in self.players:
                        if joueur_choisis == player_selected.id and player_selected.n_or > 0:
                            player.n_or += 1
                            player_selected.n_or -= 1

                    self.positionVoleur()
                else:
                    print("Aucun joueur ne possède d'or pour le moment ou le joueur sélectionner ne possède pas d'or "
                          ":( ")

    def acheteLingot(self, player):
        """
        Cette fonction propose à un joueur s'il souhaite acheter un lingot d'or pour 10 charbons.
        :param player: Il s'agit du joueur passant sur la case lingot d'or.
        :return:
        """
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

    def deplaceJoueur(self, player, lancer_de):
        """
        Cette fonction permet d'effectuer le déplacement d'un joueur. On vérifie également pendant son déplacement s'il
        tombe sur une case avec un lingot d'or, ou lorsque son tour est fini s'il est sur une case à effet.
        (voleur, swap...)
        :param player: Il s'agit du joueur actuel commençant son tour.
        :param lancer_de: Il s'agit du score de dé effecteur par le joueur indiquant le nombre de cases où il se dépplace
        :return:
        """
        player.deplacer(lancer_de, self)
        self.plateau[player.position].effet(player)
        self.Swap(player)
        self.Voleur(player)

    def tourDeJeu(self):
        """
        Cette fonction effectue un tour de jeu pour chaque joueur.
        :return:
        """
        for player in self.players:
            self.deplaceJoueur(player, lanceDe(6))

    def bonus_charbon(self):
        """
        Cette fonction permet à la fin de chaque tour de lancer un dé par joueur, celui ayant le plus haut lancé de dé
        gagne 5 charbons.
        :return:
        """
        classement = []

        for player in self.players:
            classement.append((player.id, lanceDe(100)))

        winner_player = sorted(classement, key=lambda x: x[1])
        player_to_add_charbon = winner_player[len(winner_player) - 1][0]

        for player in self.players:
            if player.id == player_to_add_charbon:
                player.charbon += 5

        print('Le vainqueur de ce tour est le joueur %s avec un score de %s, il gagne 5 charbons \n' %
              (str(winner_player[len(winner_player) - 1][0]), str(winner_player[len(winner_player) - 1][1])))

    def bonus_devine_chiffre(self):
        """
        Cette fonction demande à chaque fin de tour que les joueurs tente de deviner le chiffre choisis par l'ordinateur
        celui qui se rapprochant du chiffre ou l'ayant deviné gagne 5 charbons.
        :return:
        """
        classement = []
        ordinateur_random = lanceDe(100)

        for player in self.players:
            joueur_devine = safe_input("Entrer un chiffre entre 1 et 100 choisis, vous devinerez peut être le chiffre "
                                       "choisis aléatoirement: \n", int, lambda x: 1 <= x <= 100, non_validate_value='')

            if joueur_devine > ordinateur_random:
                resultat = joueur_devine - ordinateur_random
            else:
                resultat = ordinateur_random - joueur_devine

            classement.append((player.id, resultat))

        winner_player = sorted(classement, key=lambda x: x[1])
        player_to_add_charbon = winner_player[0][0]

        for player in self.players:
            if player.id == player_to_add_charbon:
                player.charbon += 5

        print('Le vainqueur de ce tour est le joueur %s avec une différence de %s avec le chiffre aléatoire, '
              'il gagne 5 charbons \n' %
              (str(winner_player[0][0]), str(winner_player[0][1])))

    def partie(self):
        """
        Cette fonction permet d'effectuer le démarrage de la partie en fonction du nombre de tours indiqué au début et
        à la fin de chaque tour effectue un mini-jeu (bonus charbon)
        :return:
        """
        for i in range(self.nbTours):
            self.tourDeJeu()
            self.bonus_charbon()
            self.bonus_devine_chiffre()

    def winner(self):
        """
        Cette fonction permet de trier les joueurs dans un ordre croissant indiquant le vainqueur de là
        partie (trie à bulle).
        :return:
        """
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
        """
        Cette fonction permet de sauvegarder dans un fichier .txt le classement des joueurs  lors de la partie effectuer.
        :param players: Il s'agit de la liste des joueurs de la partie.
        :return:
        """
        today = datetime.today()
        name = 'chariot-party-%s.txt' % ('-'.join(map(str, [
            today.day, today.month, today.year,
            today.hour, today.minute
        ])))  # Peut être remplacer par: name = 'chariot-party-%s.txt' % (today.strftime('%d-%m-%Y-%H-%M')
        with open(name, 'w', encoding='utf-8') as f:
            f.write(players)

    def afficheClassement(self):
        """
        Cette fonction écrit un string indiquant la position de chaque joueur à la fin de la partie.
        :return:
        """
        classement = self.winner()

        affichage = '\n'.join(["Numéro %s avec %s lingot(s) d'or et %s charbon(s)" % (
            player.id, player.n_or, player.charbon) for player in classement])

        self.sauvegardeResultats(affichage)

    def play(self):
        """
        Cette fonction permet d'effectuer le lancement d'une partie ainsi que l'enregistrement du résultat de celle-ci
        :return:
        """
        self.partie()
        self.afficheClassement()
