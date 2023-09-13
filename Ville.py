import math


class Ville:
    def __init__(self, nom, x, y):
        self.nom = nom
        self.x = x
        self.y = y

    def distance_vers(self, autre_ville):
        """
        Calcule la distance entre cette ville et une autre ville.
        """
        dx = self.x - autre_ville.x
        dy = self.y - autre_ville.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def __str__(self):
        return self.nom
