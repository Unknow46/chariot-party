# coding: utf-8

from case import Case


class CaseRouge(Case):
    def __init__(self):
        super().__init__(2)

    def effet(self, player):
        if player.charbon - 3 > 0:
            player.charbon -= 3
