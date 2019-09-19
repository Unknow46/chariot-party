# coding: utf-8

from interface_objet import *


class Joueur:
    def __init__(self, joueur_id):
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
        for i in range(n):
            self.position = (self.position + 1) % len(plat.plateau)
            bougeJoueur(self, plat.plateau)
            plat.acheteLingot(self)
