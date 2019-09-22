# coding: utf-8

from case import Case


class CaseBleue(Case):
    """
    Cette classe contient les informations de la case bleue.
    """
    def __init__(self):
        """
        Le chiffre de la case bleue est 3.
        """
        super().__init__(3)

    def effet(self, player):
        """
        Si le joueur tombe sur cette case rien ne se passe.
        :param player: joueur tombant sur la case.
        :return:
        """
        pass
