from data import *

### from a directed graph find all possible ways through it

def find_all_paths(graph, current_node, visited, path, all_paths):
    visited.add(current_node)
    path.append(current_node)

    if len(path) == len(graph):
        all_paths.append(path[:])
    else:
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                find_all_paths(graph, neighbor, visited, path, all_paths)

    visited.remove(current_node)
    path.pop()

def all_ways_to_visit_nodes(edges):
    all_paths = []
    nodes = set(edges.keys())
    for start_node in nodes:
        visited_nodes = set()
        path = []
        find_all_paths(edges, start_node, visited_nodes, path, all_paths)

    return all_paths

"""edges = {
    1: [4],
    2: [1, 3],
    3: [2],
    4: [2, 3],
}

result = all_ways_to_visit_nodes(edges)
for path in result:
    print(" -> ".join(str(node) for node in path))"""


### from a directed graph find all possible ways through it from a given starting node
best_path = []

def find_all_paths_starting_node(graph, current_node, visited, path, best_path, starting_node, dur):
    visited.add(current_node)
    path.append(current_node)

    if len(path) == len(graph) and current_node != starting_node and len(best_path) < 1:
        best_path.append(path[:])

    elif len(path) == len(graph) and current_node != starting_node and total_duration(path, dur) < total_duration(best_path[0], dur):
        best_path.pop()
        best_path.append(path[:])

    else:
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                find_all_paths_starting_node(graph, neighbor, visited, path, best_path, starting_node, dur)

    visited.remove(current_node)
    path.pop()

def all_ways_to_visit_nodes_starting_node(edges, starting_node, dur):
    #best_path = []
    nodes = set(edges.keys())
    visited_nodes = set()
    path = []
    find_all_paths_starting_node(edges, starting_node, visited_nodes, path, best_path, starting_node, dur)

    return best_path

"""edges = {
    1: [4],
    2: [1, 3],
    3: [2],
    4: [2, 3],
}

starting_node = 1
result = all_ways_to_visit_nodes_starting_node(edges, starting_node)
print(result)
for path in result:
    print(" -> ".join(str(node) for node in path))"""

