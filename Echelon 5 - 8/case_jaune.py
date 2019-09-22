# coding: utf-8

from case import Case


class CaseJaune(Case):
    """
    Cette classe indique les informations sur la case jaune
    """
    def __init__(self):
        """
        Le chiffre pour une case jaune est 4
        """
        super().__init__(4)

    def effet(self, player):
        """
        Si un joeur tombe sur une case jaune il gagne 10 charbon
        :param player: le joueur tombant sur la case jaune.
        :return:
        """
        player.charbon += 10
