import math
import itertools

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

def calculate_distance(tour, dist):
    distance = 0
    for i in range(len(tour)-1):
        distance += get_distance(tour[i], tour[i+1], dist)
    distance += get_distance(tour[-1], tour[0], dist)
    return distance

def threeOpt(tour, dist):
    best_distance = calculate_distance(tour, dist)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour)-4):
            for j in range(i+2, len(tour)-2):
                for k in range(j+2, len(tour)):
                    new_tour = tour[:i] + tour[i:j][::-1] + tour[j:k][::-1] + tour[k:]
                    new_distance = calculate_distance(new_tour, dist)
                    if new_distance < best_distance:
                        tour = new_tour
                        best_distance = new_distance
                        improved = True
                        break
                if improved:
                    break
            if improved:
                break
    return tour, best_distance



#by chatGPT
def heldKarp(graph, start_node):
    n = len(graph)
    dp = {}

    # Initialize DP table for the base case
    for i in range(n):
        if i == start_node: continue
        dp[(1 << i, i)] = (graph[start_node][i], start_node)

    # Fill in the DP table for all subproblems
    for size in range(2, n):
        for subset in itertools.combinations(range(n), size):
            if start_node not in subset: continue
            for k in subset:
                if k == start_node: continue
                state = 0
                for x in subset:
                    if x == k or x == start_node: continue
                    state |= 1 << x
                if (state, k) not in dp: continue
                for j in subset:
                    if j == k or j == start_node: continue
                    prev = dp[(state, k)]
                    new_dist = prev[0] + graph[j][k]
                    if (state | (1 << j), j) not in dp:
                        dp[(state | (1 << j), j)] = (new_dist, k)
                    elif new_dist < dp[(state | (1 << j), j)][0]:
                        dp[(state | (1 << j), j)] = (new_dist, k)

    # Find the optimal path
    min_dist = math.inf
    last = None
    for i in range(n):
        if i == start_node: continue
        dist = dp[((1 << n) - 1, i)][0] + graph[i][start_node]
        if dist < min_dist:
            min_dist = dist
            last = i

    # Reconstruct the optimal path
    path = [start_node, last]
    state = (1 << n) - 1
    while path[-1] != start_node:
        next_node = dp[(state, last)][1]
        state ^= 1 << last
        last = next_node
        path.append(last)
    return (min_dist, path)

def algorithm(algorithm_name, tour, dist):
    if algorithm_name == "twoOpt":
        tour = twoOpt(tour, dist)
    """elif algorithm_name == "heldKarp":
        print(algorithm_name)
        start = 1
        min_dist, path = heldKarp(graph, start)
        print("The distance is {}".format(min_dist))"""
    return tour
