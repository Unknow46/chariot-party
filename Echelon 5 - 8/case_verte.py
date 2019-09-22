# coding: utf-8

from case import Case


class CaseVerte(Case):
    """
    Cette classe contient les informations de la case verte
    """
    def __init__(self):
        """
        Le chiffre de la case verte est 1
        """
        super().__init__(1)

    def effet(self, player):
        """
        Si un joueur tombe sur la case verte il gagne 1 charbon
        :param player: le joueur tombant sur la case
        :return:
        """
        player.charbon += 1
