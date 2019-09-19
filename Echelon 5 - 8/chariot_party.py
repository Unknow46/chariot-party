# coding: utf-8

from plateau import Plateau

plateau = []
players = []

nbJoueurs = 0
nbTours = 0
nbCases = 0
gold = 0

if __name__ == '__main__':
    start_game = Plateau(plateau, players, nbJoueurs, nbCases, gold)
    start_game.play()
