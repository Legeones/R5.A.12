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


def lancer_et_generer_graphique(nb_iterations, nb_echantillons, affichage=False):
    """

    :param nb_iterations: nombre d'itérations effectué par l'algorithme
    :param nb_echantillons: population de chemins initiale
    :param affichage: booléen si l'affichage des graphiques se fait à chaque itération de paramètres
    """
    parametres = [(0.02, 0.7), (0.05, 0.8), (0.1, 0.9)]  # Différents paramètres de mutation et de croisement
    diversites = []  # Liste pour stocker les diversités à chaque itération pour chaque paramètre
    echan = Echantillon()
    echan.generer_villes_aleatoires(50, 0, 50, 0, 50)
    villes1 = echan.villes
    algo = AlgorithmesGenetiques(None, nb_echantillons, villes1)
    population = algo.echantillion.chemins
    for mutation_rate, crossover_rate in parametres:
        algo.echantillion.chemins = population
        algo.lancer(0.1, crossover_rate, nb_iterations, mutation_rate)
        diversites.append(algo.diversite_final)

    # Créer un graphique pour chaque ensemble de paramètres
    plt.figure(figsize=(10, 6))
    for i, (mutation_rate, crossover_rate) in enumerate(parametres):
        plt.plot(range(len(diversites[i])), diversites[i],
                 label=f'Mutation: {mutation_rate}, Croisement: {crossover_rate}')

    plt.xlabel('Nombre d\'itérations')
    plt.ylabel('Diversité')
    plt.title('Évolution de la diversité pour différents paramètres')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    nb_villes = 20
    echan = Echantillon()
    # pm = [0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    # pc = [0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    echan.generer_villes_aleatoires(nb_villes, 0, 50, 0, 50)
    echan.affichageVilles()
    villes = echan.villes
    algo = AlgorithmesGenetiques(None, 400, villes)
    thread1 = threading.Thread(target=algo.lancer, args=(0.5, 0.85, 200, 0.02, True))
    manager = enlighten.Manager()
    # popGen1 = pow(nb_villes, 2)
    # algoGen1 = AlgorithmesGenetiques(nb_villes, popGen1, villes)
    if nb_villes <= 13:
        algo3 = threading.Thread(target=exhaustive_search, args=(villes, 3, manager))
    else:
        algo3 = None
    # algoGen2 = AlgorithmesGenetiques(nb_villes, 100, villes)
    # # algo.lancer(100, 100, 400)
    # algo1 = LauncherThread(1, algoGen1, popGen1//10, popGen1//10, 100, manager)
    # algo2 = LauncherThread(2, algoGen2, 50, 50, 900, manager)
    # algo1.start()
    # algo2.start()
    # thread1.start()
    if algo3 is not None: algo3.start()
    # algo1.join()
    # algo2.join()
    # thread1.join()
    if algo3 is not None: algo3.join()
    lancer_et_generer_graphique(100, 200)
