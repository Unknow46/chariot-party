# coding: utf-8


class Case:
    """
    Cette classe correspond à la case de défaut (blanche)
    """
    def __init__(self, couleur=0):
        self.couleur = couleur

    def effet(self, players):
        raise Exception("Fonction non implémenter pour la couleur %s." % self.couleur)
