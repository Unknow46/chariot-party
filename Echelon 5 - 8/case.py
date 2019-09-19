# coding: utf-8


class Case:
    def __init__(self, couleur=0):
        self.couleur = couleur

    def effet(self, players):
        raise Exception("Fonction non implémenter pour la couleur %s." % (self.couleur))
