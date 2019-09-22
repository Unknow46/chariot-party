# coding: utf-8

from interface_objet import *


class Joueur:
    """
    Il s'agit de la classe comportant les informations de chaque joeurs, elle permet également d'effectuer leur
    déplacement sur le plateau.
    """
    def __init__(self, joueur_id):
        """
        Il s'agit de l'initialisation de chaque joueur dans la partie
        :param joueur_id: numéro du joeur pouvant aller de 0 à 4
        """
        self.id = joueur_id
        self.position = 0
        self.charbon = 5
        self.n_or = 0

    def __lt__(self, joueur):  # For x < y

        if joueur.n_or == self.n_or:
            return self.charbon < joueur.charbon
        return self.n_or < joueur.n_or

    def __le__(self, joueur):  # For x <= y
        return self < joueur or self == joueur

    def __eq__(self, joueur):  # For x == y
        return self.n_or == joueur.n_or and self.charbon and joueur.charbon

    def __ne__(self, joueur):  # For x != y OR x <> y
        return not self == joueur

    def __gt__(self, joueur):  # For x > y
        if joueur.n_or == self.n_or:
            return self.charbon > joueur.charbon
        return self.n_or > joueur.n_or

    def __ge__(self, joueur):  # For x >= y
        return self > joueur or self == joueur

    def deplacer(self, n, plat):
        """
        Cette fonction effectue un déplacement du joueur case par case, il vérifie en même temps si celui-ci passe par
        la case lingot d'or et regarde s'il peut en acheter un.
        :param n: Il s'agit du lancé de dé effectué par le joueur indiquant le nombre de cases où il doit se déplacer.
        :param plat: Il s'agit du plateau
        :return:
        """
        for i in range(n):
            self.position = (self.position + 1) % len(plat.plateau)
            bougeJoueur(self, plat.plateau)
            plat.acheteLingot(self)
