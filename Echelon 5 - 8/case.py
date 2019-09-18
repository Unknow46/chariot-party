# coding: utf-8


class Case:
    def __init__(self, couleur):
        self.couleur = couleur

    def effet(self, player):
        if self.couleur == 1:
            player.charbon += 3
        elif self.couleur == 2 and player.charbon - 3 > 0:
            player.charbon -= 3
