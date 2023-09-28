class Chemin:
    def __init__(self, villes):
        self.villes = villes  # Une liste d'objets Ville

    def longueur(self):
        """
        Calcule la longueur totale du chemin.
        """
        longueur = 0
        for i in range(len(self.villes) - 1):
            longueur += self.villes[i].distance_vers(self.villes[i+1])
        # Ajoute la distance de retour à la première ville pour former une boucle
        longueur += self.villes[-1].distance_vers(self.villes[0])
        return longueur

    def matrice_distances(self):
        """
        Crée et renvoie une matrice de distances entre les villes dans l'échantillon.
        """
        n = len(self.villes)
        matrice = [[0] * n for _ in range(n)]

        for i in range(n):
            for j in range(i + 1, n):
                distance = self.villes[i].distance_vers(self.villes[j])
                matrice[i][j] = distance
                matrice[j][i] = distance

        return matrice



    def __str__(self):
        noms_villes = [str(ville) for ville in self.villes]
        return ' -> '.join(noms_villes) + f' -> {self.villes[0]}'  # Pour former une boucle