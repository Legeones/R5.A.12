import threading
import itertools
import sys
import time

import enlighten

from Chemin import Chemin
from Echantillion import Echantillon
import random


# ... Votre code précédent ...

def afficher_progression(pourcentage):
    barre = "#" * int(pourcentage / 2)
    sys.stdout.write("\r[%-50s] %d%%" % (barre, pourcentage))
    sys.stdout.flush()


# ... Votre code précédent ...

class LauncherThread(threading.Thread):
    def __init__(self, identifiant, algo, nb_selection, nb_fusion, nb_iterations, manager):
        super().__init__()
        self.algo = algo
        self.nb_selection = nb_selection
        self.nb_fusion = nb_fusion
        self.nb_iterations = nb_iterations
        self.verrou = threading.Lock()  # Chaque thread a son propre verrou
        self.manager = manager
        self.identifiant = identifiant

    def run(self):
        with self.manager.counter(total=self.nb_iterations, unit='iterations', color='green', desc=f'Thread-{self.identifiant}') as progress:
            t1 = time.time()
            distances = self.algo.liste_distance_chemins()
            actuel_min = min(distances, key=distances.get)
            min_total = actuel_min
            min_list = [min_total.longueur()]

            for i in range(self.nb_iterations):
                self.algo.selection_par_roulette(self.nb_selection)
                self.algo.effectuer_fusion(self.nb_fusion)
                self.algo.effectuer_mutation(0.005)
                distances = self.algo.liste_distance_chemins()
                actuel_min = min(distances, key=distances.get)
                min_total = actuel_min if actuel_min.longueur() < min_total.longueur() else min_total
                if min_list[-1] != min_total.longueur():
                    min_list.append(min_total.longueur())
                progress.update()

            temps_ecoule = time.time() - t1
            print(f"Temps écoulé pour Thread-{self.identifiant}: {temps_ecoule:.2f} secondes")
            print(f"Chemin minimum obtenu pour Thread-{self.identifiant}: longueur {min_total.longueur()}, {min_total}")
            print(min_list)
