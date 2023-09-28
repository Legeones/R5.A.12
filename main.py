from AlgorithmeGenetique import AlgorithmesGenetiques
from Echantillion import Echantillon

M = [[0, 1, 2, 3, 4, 5, 6],
     [1, 0, 4, 6, 1, 8, 9],
     [2, 4, 0, 4, 2, 9, 4],
     [3, 6, 4, 0, 5, 8, 1],
     [4, 1, 2, 5, 0, 5, 6],
     [5, 8, 9, 8, 5, 0, 3],
     [6, 9, 4, 1, 6, 3, 0]]

parcours = [[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]]

if __name__ == '__main__':
    algo = AlgorithmesGenetiques(50, 200)
    algo.lancer(100, 100, 400)
