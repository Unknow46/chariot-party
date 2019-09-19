# coding: utf-8

from case import Case


class CaseJaune(Case):
    def __init__(self):
        super().__init__(4)

    def effet(self, player):
        player.charbon += 10
