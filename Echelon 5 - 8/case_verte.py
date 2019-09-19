# coding: utf-8

from case import Case


class CaseVerte(Case):
    def __init__(self):
        super().__init__(1)

    def effet(self, player):
        player.charbon += 1
