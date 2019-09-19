# coding: utf-8

from case_verte import CaseVerte
from case_rouge import CaseRouge
from case_bleue import CaseBleue
from case_jaune import CaseJaune

VERT, ROUGE, BLEU, JAUNE = 1, 2, 3, 4


class FabriqueCase():
    couleurs = {
        VERT: CaseVerte,
        ROUGE: CaseRouge,
        BLEU: CaseBleue,
        JAUNE: CaseJaune,
    }

    def create(self, couleur):
        if not FabriqueCase.couleurs.get(couleur):
            raise Exception("La couleur %s n'est pas valide !")
        return FabriqueCase.couleurs[couleur]()
