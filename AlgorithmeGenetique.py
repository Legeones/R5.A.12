import itertools
import sys
import time

import enlighten
from tqdm import tqdm

from Chemin import Chemin
from Echantillion import Echantillon
import random


def exhaustive_search(ensemble_villes, identifiant, manager):
    t1 = time.time()
    meilleur_chemin = None
    meilleure_longueur = float('inf')  # Initialisation à une valeur infinie

    n = len(ensemble_villes)
    indices = list(range(n))
    permutations = []

    total_permutations = 1
    for i in range(1, n + 1):
        total_permutations *= i
    # Génération de toutes les permutations possibles des villes
    permutations = list(tqdm(itertools.permutations(ensemble_villes), desc="Permutations", unit=" permutation", total=total_permutations))
    with manager.counter(total=len(permutations), unit='iterations', color='green',
                         desc=f'Thread-{identifiant}') as progress:
        for permutation in permutations:
            chemin = Chemin(list(permutation))  # Création d'un chemin avec la permutation
            longueur = chemin.longueur()  # Calcul de la longueur du chemin
            progress.update()
            # Mise à jour du meilleur chemin si nécessaire
            if longueur < meilleure_longueur:
                meilleure_longueur = longueur
                meilleur_chemin = chemin
        progress.close()
    temps_ecoule = time.time() - t1
    print(f"Temps : {temps_ecoule}, distance {meilleure_longueur}")
    return meilleur_chemin, meilleure_longueur


class AlgorithmesGenetiques:
    def __init__(self, nb_villes=None, nb_population=None, villes=None):
        self.echantillion = Echantillon()
        if villes is not None:
            self.echantillion.creer_echantillion(nb_villes, nb_population, villes)
        else:
            self.echantillion.creer_echantillion(nb_villes, nb_population, None)

    def selection_par_roulette(self, nombre_selectionnes):
        # Calculez la somme totale des valeurs de fitness des chemins
        somme_fitness = sum(1 / chemin.longueur() for chemin in self.echantillion.chemins)
        # Sélectionnez des chemins proportionnellement à leur fitness
        chemins_selectionnes = Echantillon()
        for _ in range(nombre_selectionnes):
            # Séléction aléatoire d'une somme_fitness_temporaire à l'instant t
            choix = random.uniform(0, somme_fitness)
            somme_partielle = 0
            for chemin in self.echantillion.chemins:
                # Valeur fitness du chemin en cours
                somme_partielle += 1 / chemin.longueur()
                # Si le chemin est meilleur que le choix on le prend
                if somme_partielle >= choix:
                    chemins_selectionnes.ajouter_chemin(chemin)
                    break
        self.echantillion = chemins_selectionnes

    def fusionner_chemins(self, parents):
        enfants = []

        # Choisissez un point de croisement aléatoire (crossover point)

        for _ in range(2):  # Créez deux enfants à chaque fusion
            point_de_croisement = random.randint(1, len(parents[0].villes) - 1)
            enfant_villes = (list)
            enfant_villes = parents[0].villes[:point_de_croisement]
            for index, i in enumerate(parents[1].villes[point_de_croisement:]):
                if i not in enfant_villes:
                    enfant_villes.append(i)
            for i in self.echantillion.villes:
                if i not in enfant_villes:
                    enfant_villes.append(i)
            enfant = Chemin(enfant_villes)
            enfants.append(enfant)

        return enfants

    def effectuer_fusion(self, nombre_parents_fusiones):
        # Sélectionnez des paires de parents pour la fusion
        chemins_parents = random.sample(self.echantillion.chemins, nombre_parents_fusiones)

        nouveaux_chemins = []
        for i in range(0, len(chemins_parents), 2):
            parents = chemins_parents[i:i + 2]
            enfants = self.fusionner_chemins(parents)
            nouveaux_chemins.extend(enfants)

        # Remplacez une partie des chemins existants par les nouveaux chemins créés
        # self.echantillion.chemins = random.sample(self.echantillion.chemins,
        #                                           len(self.echantillion.chemins) - nombre_fusions)
        self.echantillion.chemins.extend(nouveaux_chemins)

    def effectuer_mutation(self, taux):
        for chemin in self.echantillion.chemins:
            if random.random() < taux:
                # print("Mutation")
                nb_villes = len(chemin.villes)
                index1, index2 = 0, 0
                while index1 == 0 or index2 == 0:
                    index1, index2 = random.sample(range(nb_villes), 2)
                chemin.villes[index1], chemin.villes[index2] = chemin.villes[index2], chemin.villes[index1]

    def moyenne_distance_tour(self):
        som = 0
        i = (Chemin)
        for i in self.echantillion.chemins:
            som += i.longueur()
        return som / len(self.echantillion.chemins)

    def liste_distance_chemins(self):
        distances = {}
        for chemin in self.echantillion.chemins:
            distances[chemin] = chemin.longueur()
        return distances

    def lancer(self, nb_selection, nb_fusion, nb_iterations, affichage=False):
        t1 = time.time()
        distances = self.liste_distance_chemins()
        actuel_min = min(distances, key=distances.get)
        min_total = actuel_min
        min_list = [min_total.longueur()]
        if affichage:
            print(f"Minimum actuel {min_total}.")
        for i in range(nb_iterations):
            pourcentage = i / nb_iterations * 100
            barre = "#" * int(pourcentage / 2)
            sys.stdout.write("\r[%-50s] %d%%" % (barre, pourcentage))
            sys.stdout.flush()
            self.selection_par_roulette(nb_selection)
            self.effectuer_fusion(nb_fusion)
            self.effectuer_mutation(0.005)
            distances = self.liste_distance_chemins()
            actuel_min = min(distances, key=distances.get)
            min_total = actuel_min if actuel_min.longueur() < min_total.longueur() else min_total
            if min_list[-1] != min_total.longueur():
                min_list.append(min_total.longueur())
            if affichage:
                print(f"Minimum actuel {min_total.longueur()}.")
                print(f"Longueur moyenne {i} : ")
                print(actuel_min.longueur())
                print("\n")
        temps_ecoule = time.time() - t1
        print(f"Temps écoulé : {temps_ecoule} secondes")
        print(f"Chemin minimum obtenu : longueur {min_total.longueur()}, {min_total}")
        print(min_list)
