import math
import itertools

# twoOpt algorithm
def twoOpt(tour, dist):
    start = tour[0]
    finish = tour[1]

    improvement = True
    while improvement:
        improvement = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour) - 1):
                dist_original = dist[tour[i - 1]][tour[i]] + \
                                dist[tour[j]][tour[j + 1]]
                dist_test = dist[tour[i - 1]][tour[j]] + dist[tour[i]][tour[j + 1]]
                if dist_test < dist_original:
                    tour[i:j + 1] = reversed(tour[i:j + 1])
                    improvement = True
    return tour

def get_distance(node1, node2, dist):
    return dist[node1-1][node2-1]

# calculates total distance of a given tour
def calculate_distance(tour, dist):
    distance = 0
    for i in range(len(tour)-1):
        distance += get_distance(tour[i], tour[i+1], dist)
    distance += get_distance(tour[-1], tour[0], dist)
    return distance

# choose between algorithms
def algorithm(algorithm_name, tour, dist):
    if algorithm_name == "twoOpt":
        tour = twoOpt(tour, dist)

    ### insert other algorithms
    return tour
