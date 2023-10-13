# Importation des modules nécessaires
import itertools
import math
import sys
import time
import matplotlib.pyplot as plt
import enlighten
from tqdm import tqdm
from Chemin import Chemin
from Echantillion import Echantillon
import random
import numpy as np


# Fonction pour la recherche exhaustive du TSP
def exhaustive_search(ensemble_villes, identifiant, manager):
    # Initialisation des variables
    t1 = time.time()
    meilleur_chemin = None
    meilleure_longueur = float('inf')  # Initialisation à une valeur infinie

    n = len(ensemble_villes)
    indices = list(range(n))

    # Fixer la ville de départ (WUO dans cet exemple)
    indices.remove(0)

    # Génération de toutes les permutations possibles des villes
    permutations = list(tqdm(itertools.permutations(indices), desc="Permutations", unit=" permutation",
                             total=math.factorial(n - 1)))

    # Recherche du meilleur chemin parmi les permutations
    with manager.counter(total=len(permutations), unit='iterations', color='green',
                         desc=f'Thread-{identifiant}') as progress:
        for permutation in permutations:
            chemin_indices = [0] + list(permutation)
            chemin = Chemin([ensemble_villes[i] for i in chemin_indices])  # Création d'un chemin avec la permutation
            longueur = chemin.longueur()  # Calcul de la longueur du chemin
            progress.update()
            # Mise à jour du meilleur chemin si nécessaire
            if longueur < meilleure_longueur:
                meilleure_longueur = longueur
                meilleur_chemin = chemin
        progress.close()

    # Affichage du temps d'exécution et du meilleur chemin trouvé
    temps_ecoule = time.time() - t1
    print(f"Temps : {temps_ecoule}, distance {meilleure_longueur}")
    echan = Echantillon()
    echan.villes = ensemble_villes
    echan.affichageVilles(meilleur_chemin.villes)
    print(meilleur_chemin)
    return meilleur_chemin, meilleure_longueur


# Fonction pour créer un graphique de l'évolution des distances des chemins
def graphLongueurs(liste_min_tour, liste_min_total):
    plt.figure(figsize=(10, 6))  # Ajuster la taille de la figure selon votre préférence
    for i in range(len(liste_min_tour) - 1):
        plt.plot([i, i + 1], [liste_min_tour[i], liste_min_tour[i + 1]], color='green')
    for i in range(len(liste_min_total) - 1):
        plt.plot([i, i + 1], [liste_min_total[i], liste_min_total[i + 1]], color='red')
    plt.title("Représentation graphique de l'évolution de la distance")
    plt.ylabel('Distance')
    plt.xlabel('Itérations')
    plt.show()  # Afficher le graphique


# Fonction pour créer un graphique de l'évolution de la diversité de la population
def graphDiversite(diversite_liste):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(diversite_liste) + 1), diversite_liste, marker='o', color='b', linestyle='-', linewidth=2)
    plt.xlabel('Nombre d\'itérations')
    plt.ylabel('Diversité')
    plt.title('Évolution de la diversité de la population')
    plt.grid(True)
    plt.show()


# Classe pour implémenter les algorithmes génétiques pour le TSP
class AlgorithmesGenetiques:
    def __init__(self, nb_villes=None, nb_population=None, villes=None):
        self.echantillion = Echantillon()
        self.diversite_final = []
        # Création de l'échantillon initial
        if villes is not None:
            self.echantillion.creer_echantillion(nb_villes, nb_population, villes)
        else:
            self.echantillion.creer_echantillion(nb_villes, nb_population, None)

    # Méthode de sélection des chemins par roulette
    def selection_par_roulette(self, nombre_selectionnes):
        # Calcul de la somme totale des valeurs de fitness des chemins
        somme_fitness = sum(1 / chemin.longueur() for chemin in self.echantillion.chemins)
        # Sélection des chemins proportionnellement à leur fitness
        chemins_selectionnes = Echantillon()
        for _ in range(nombre_selectionnes):
            choix = random.uniform(0, somme_fitness)  # Choix d'une somme fitness temporaire aléatoire
            somme_partielle = 0
            for chemin in self.echantillion.chemins:
                somme_partielle += 1 / chemin.longueur()  # Fitness du chemin en cours
                # Si le chemin est meilleur que le choix, il est sélectionné
                if somme_partielle >= choix:
                    chemins_selectionnes.ajouter_chemin(chemin)
                    break
        return chemins_selectionnes.chemins

    # Méthode de sélection des chemins par taux
    def selection_par_taux(self, taux_selection=0.85):
        somme_fitness = sum(1 / chemin.longueur() for chemin in self.echantillion.chemins)
        nombre_selectionnes = int(taux_selection * len(self.echantillion.chemins))
        # Tri des chemins par fitness (du meilleur au pire)
        chemins_tries = sorted(self.echantillion.chemins, key=lambda chemin: 1 / chemin.longueur())
        # Sélection des meilleurs individus en fonction du taux spécifié
        chemins_selectionnes = Echantillon()
        for chemin in chemins_tries[:nombre_selectionnes]:
            chemins_selectionnes.ajouter_chemin(chemin)
        return chemins_selectionnes.chemins

    # Méthode pour fusionner les chemins parents et créer des enfants
    def fusionner_chemins(self, parents):
        enfants = []
        # Choix d'un point de croisement aléatoire
        for _ in range(2):  # Création de deux enfants à chaque fusion
            point_de_croisement = random.randint(1, len(parents[0].villes) - 1)
            enfant_villes = list(parents[0].villes[:point_de_croisement])
            for index, i in enumerate(parents[1].villes[point_de_croisement:]):
                if i not in enfant_villes:
                    enfant_villes.append(i)
            for i in self.echantillion.villes:
                if i not in enfant_villes:
                    enfant_villes.append(i)
            enfant = Chemin(enfant_villes)
            enfants.append(enfant)
        return enfants

    # Méthode pour effectuer la fusion des chemins en fonction d'un taux de croisement
    def effectuer_fusion(self, taux_croisement=0.85):
        """

        :param taux_croisement: Taux auquel l'algorithme selectionne les individus donc 85%
        """
        nombre_parents_croises = int(taux_croisement * len(self.echantillion.chemins))
        nombre_parents_croises += 1 if nombre_parents_croises % 2 != 0 else 0
        chemins_parents = self.selection_par_roulette(nombre_parents_croises)
        nouveaux_chemins = []
        for i in range(0, len(chemins_parents), 2):
            parents = chemins_parents[i:i + 2]
            enfants = self.fusionner_chemins(parents)
            nouveaux_chemins.extend(enfants)
        # Remplacement des individus excédentaires parmi les moins performants
        nouveaux_chemins.sort(key=lambda chemin: chemin.longueur(),
                              reverse=True)  # Tri des nouveaux chemins par performance (du pire au meilleur)
        self.echantillion.chemins = (
                self.echantillion.chemins[:len(self.echantillion.chemins) - len(nouveaux_chemins)] +
                nouveaux_chemins[:len(self.echantillion.chemins)])
        # Assurer que la population reste de même taille
        assert len(self.echantillion.chemins) == self.echantillion.taille_pop_origin

    # Méthode pour effectuer la mutation des chemins
    def effectuer_mutation(self, taux):
        for chemin in self.echantillion.chemins:
            if random.random() < taux:
                nb_villes = len(chemin.villes)
                index1, index2 = 0, 0
                while index1 == 0 or index2 == 0:
                    index1, index2 = random.sample(range(nb_villes), 2)
                chemin.villes[index1], chemin.villes[index2] = chemin.villes[index2], chemin.villes[index1]

    # Méthode pour calculer la moyenne de la distance des chemins dans la population
    def moyenne_distance_tour(self):
        som = 0
        for chemin in self.echantillion.chemins:
            som += chemin.longueur()
        return som / len(self.echantillion.chemins)

    # Méthode pour créer un dictionnaire des distances des chemins dans la population
    def liste_distance_chemins(self):
        distances = {}
        for chemin in self.echantillion.chemins:
            distances[chemin] = chemin.longueur()
        return distances

    # Méthode pour calculer et retourner l'indicateur de diversité génétique de la population actuelle
    def calculer_diversite(self):
        distances = [chemin.longueur() for chemin in self.echantillion.chemins]
        variance = np.var(distances)
        return variance

    # Méthode principale pour lancer l'algorithme génétique
    def lancer(self, nb_selection, nb_fusion, nb_iterations, mutation, affichage=False):
        t1 = time.time()
        distances = self.liste_distance_chemins()
        actuel_min = min(distances, key=distances.get)
        min_total = actuel_min
        min_total_list = [min_total.longueur()]
        min_list = [min_total.longueur()]
        diversite_actuelle = self.calculer_diversite()
        diversite_total_list = [diversite_actuelle]
        if affichage:
            print(f"Minimum actuel {min_total}.")
        # Boucle principale pour les itérations de l'algorithme génétique
        for i in range(nb_iterations):
            pourcentage = i / nb_iterations * 100
            barre = "#" * int(pourcentage / 2)
            sys.stdout.write("\r[%-50s] %d%%" % (barre, pourcentage))
            sys.stdout.flush()
            self.effectuer_fusion(nb_fusion)  # Effectuer la fusion des chemins
            self.effectuer_mutation(mutation)  # Effectuer la mutation des chemins
            distances = self.liste_distance_chemins()
            actuel_min = min(distances, key=distances.get)
            # Mettre à jour le meilleur chemin si un chemin plus court est trouvé
            min_total = actuel_min if actuel_min.longueur() < min_total.longueur() else min_total
            min_list.append(actuel_min.longueur())
            min_total_list.append(min_total.longueur())
            diversite_actuelle = self.calculer_diversite()
            diversite_total_list.append(diversite_actuelle)
        self.diversite_final = diversite_total_list
        temps_ecoule = time.time() - t1
        print(f"Temps écoulé : {temps_ecoule / 60} minutes")
        print(f"Chemin minimum obtenu : longueur {min_total.longueur()}, {min_total}")
        graphLongueurs(min_list, min_total_list)  # Afficher le graphique de l'évolution des distances
        if affichage:
            graphDiversite(diversite_total_list)  # Afficher le graphique de l'évolution de la diversité
            self.echantillion.affichageVilles(min_total.villes)  # Afficher le chemin sur la carte des villes
