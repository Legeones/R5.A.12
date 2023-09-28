import random
import string

from Chemin import Chemin
from Ville import Ville


class Echantillon:
    def __init__(self):
        self.chemins = []
        self.villes = []

    def creer_echantillion(self, nb_villes, nb_population):
        self.generer_villes_aleatoires(nb_villes, 0, nb_villes, 0, nb_villes)
        for i in range(nb_population):
            self.ajouter_chemin(self.creer_chemin_aleatoire())

    def ajouter_chemin(self, chemin):
        self.chemins.append(chemin)
        self.maj_villes(chemin)

    def maj_villes(self, chemin):
        for ville in chemin.villes:
            if ville not in self.villes:
                self.villes.append(ville)

    def generer_villes_aleatoires(self, nombre_de_villes, x_min, x_max, y_min, y_max):
        """
        Génère un nombre spécifié de villes aléatoires avec des coordonnées uniques
        limitées par x_min, x_max, y_min et y_max.
        """
        while len(self.villes) < nombre_de_villes:
            nom_ville = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))  # Génère un nom aléatoire de 3 caractères
            x = random.uniform(x_min, x_max)
            y = random.uniform(y_min, y_max)
            nouvelle_ville = Ville(nom_ville, x, y)
            if nouvelle_ville not in self.villes:
                self.villes.append(nouvelle_ville)

    def matrice_distances(self):
        """
        Crée et renvoie une matrice de distances entre les villes dans l'échantillon.
        """
        n = len(self.villes)
        matrice = [[0] * n for _ in range(n)]

        for i in range(n):
            for j in range(i + 1, n):
                distance = self.villes[i].distance_vers(self.villes[j])
                matrice[i][j] = round(distance, 2)
                matrice[j][i] = round(distance, 2)
        print([ville.nom for ville in self.villes])
        for j in matrice:
            print(j)

        return matrice

    def creer_chemin_aleatoire(self):
        """
        Crée un chemin aléatoire qui visite toutes les villes une fois.
        """
        echan = list(self.villes)
        ville_depart = echan.pop(0)
        villes_non_visitees = echan
        random.shuffle(villes_non_visitees)
        villes_non_visitees.insert(0, ville_depart)
        chemin_aleatoire = Chemin(villes_non_visitees)
        return chemin_aleatoire

    def __str__(self):
        return "\n".join([f"Chemin {i}: {chemin} (Longueur: {chemin.longueur()})" for i, chemin in enumerate(self.chemins)])