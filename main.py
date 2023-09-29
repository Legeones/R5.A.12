import threading

from AlgorithmeGenetique import *
from LauncherThread import LauncherThread
import enlighten

M = [[0, 1, 2, 3, 4, 5, 6],
     [1, 0, 4, 6, 1, 8, 9],
     [2, 4, 0, 4, 2, 9, 4],
     [3, 6, 4, 0, 5, 8, 1],
     [4, 1, 2, 5, 0, 5, 6],
     [5, 8, 9, 8, 5, 0, 3],
     [6, 9, 4, 1, 6, 3, 0]]

parcours = [[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]]

if __name__ == '__main__':
    echan = Echantillon()
    nb_villes = 10
    echan.generer_villes_aleatoires(nb_villes, 0, 50, 0, 50)
    villes = echan.villes
    manager = enlighten.Manager()
    popGen1 = pow(nb_villes, 2)
    algoGen1 = AlgorithmesGenetiques(nb_villes, popGen1, villes)
    if nb_villes <= 12:
        algo3 = threading.Thread(target=exhaustive_search, args=(villes, 3, manager))
    else:
        algo3 = None
    algoGen2 = AlgorithmesGenetiques(nb_villes, 100, villes)
    # algo.lancer(100, 100, 400)
    algo1 = LauncherThread(1, algoGen1, popGen1//10, popGen1//10, 100, manager)
    algo2 = LauncherThread(2, algoGen2, 50, 50, 900, manager)
    algo1.start()
    algo2.start()
    if algo3 is not None: algo3.start()
    algo1.join()
    algo2.join()
    if algo3 is not None: algo3.join()
