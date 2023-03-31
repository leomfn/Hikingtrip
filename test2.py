import numpy as np
from algorithms import *
from tour_eval import *

### test2.py = threeOpt

with open('data/osrm_distances.json') as f:
    osrm_dist = json.load(f)

def get_distance(node1, node2, distance_matrix):
    return distance_matrix[node1-1][node2-1]

def calculate_distance(tour, distance_matrix):
    distance = 0
    for i in range(len(tour)-1):
        distance += get_distance(tour[i], tour[i+1], distance_matrix)
    distance += get_distance(tour[-1], tour[0], distance_matrix)
    return distance

def three_opt(tour, distance_matrix):
    best_distance = calculate_distance(tour, distance_matrix)
    improved = True
    i = 1
    while improved:
        improved = False
        best_segment = None
        for j in range(i, len(tour)-4):
            print(i)
            for k in range(j+2, len(tour)-2):
                for l in range(k+2, len(tour)):
                    new_tour = tour[:j+1] + tour[k:l][::-1] + tour[j+1:k] + tour[l:]
                    new_distance = calculate_distance(new_tour, distance_matrix)
                    if new_distance < best_distance:
                        best_distance = new_distance
                        best_segment = (j+1, k, l)
                        improved = True
            if improved:
                break
        if improved:
            tour[best_segment[0]:best_segment[1]] = tour[best_segment[0]:best_segment[1]][::-1]
            tour[best_segment[1]:best_segment[2]] = tour[best_segment[1]:best_segment[2]][::-1]
            i = best_segment[0]
        else:
            break
    return tour, best_distance

# Example with 222 nodes
distance_matrix = np.array(osrm_dist)
initial_tour = [9, 177, 125, 33, 20, 176, 213, 66, 126, 14, 63, 214, 70, 32, 5, 193, 98, 95, 215, 156, 184, 210, 110, 188, 189, 82, 72, 172, 40, 136, 201, 55, 207, 94, 128, 115, 17, 73, 174, 222, 118, 77, 134, 7, 49, 211, 150, 120, 16, 216, 6, 41, 53, 181, 192, 127, 137, 140, 64, 160, 123, 50, 199, 97, 46, 37, 135, 179, 157, 30, 91, 79, 83, 220, 186, 61, 68, 103, 89, 138, 159, 147, 21, 167, 116, 143, 168, 209, 58, 78, 69, 67, 146, 145, 119, 165, 12, 54, 27, 183, 221, 1, 108, 153, 34, 99, 175, 114, 87, 43, 38, 11, 19, 101, 148, 122, 151, 45, 90, 173, 44, 139, 102, 74, 121, 197, 164, 76, 59, 39, 35, 195, 3, 196, 161, 93, 198, 96, 84, 62, 202, 162, 4, 48, 190, 29, 23, 80, 71, 185, 219, 217, 36, 178, 92, 191, 206, 132, 130, 182, 52, 200, 163, 208, 18, 56, 88, 194, 218, 205, 22, 133, 155, 10, 26, 15, 117, 111, 169, 187, 2, 131, 170, 31, 13, 142, 57, 180, 203, 51, 154, 129, 152, 42, 106, 124, 65, 60, 86, 171, 109, 47, 107, 158, 144, 149, 141, 81, 75, 25, 105, 113, 24, 204, 112, 8, 85, 100, 212, 28, 104, 166]


optimized_tour, optimized_distance = three_opt(initial_tour, distance_matrix)
print("Optimized tour:", optimized_tour)
print("Optimized distance:", optimized_distance)