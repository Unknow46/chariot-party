# coding: utf-8

from case_verte import CaseVerte
from case_rouge import CaseRouge
from case_bleue import CaseBleue
from case_jaune import CaseJaune

VERT, ROUGE, BLEU, JAUNE = 1, 2, 3, 4


class FabriqueCase:
    """
    Cette classe permet de créer les différentes cases du plateau.
    """
    couleurs = {
        VERT: CaseVerte,
        ROUGE: CaseRouge,
        BLEU: CaseBleue,
        JAUNE: CaseJaune,
    }

    def create(self, couleur):
        """
        Cette fonction permet de sélectionner la case en question en fonction du chiffre indiqué (couleur), pour cela,
        elle utilise différentes classes comportant chacune une couleur précise.
        :param couleur: Il s'agit d'un chiffre compris entre 1 et 4 qui correspond à chaque case du plateau.
        :return: la case à rajouté sur le plateau.
        """
        if not FabriqueCase.couleurs.get(couleur):
            raise Exception("La couleur %s n'est pas valide !")
        return FabriqueCase.couleurs[couleur]()
