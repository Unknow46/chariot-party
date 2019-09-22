# coding: utf-8

from case import Case


class CaseRouge(Case):
    """
    Cette classe indique les informations concernant la case rouge
    """
    def __init__(self):
        """
        La chiffre pour une case rouge est 2
        """
        super().__init__(2)

    def effet(self, player):
        """
        Si le joueur tombe sur une case rouge il perd 3 charbons
        :param player: joeur tombant sur la carte
        :return:
        """
        if player.charbon - 3 > 0:
            player.charbon -= 3
