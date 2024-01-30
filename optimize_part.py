import json
from possible_ways import *
from data import *
import time


#start time measurement
start_time = time.time()

#load duration and distance matrix
#load dictionary with edges (5 nearest or determined by previous runs

decision = "R"

if decision == "R":
    points = getWayPoints()
    pointids = list(points.keys())
    dist, dur = getDistAndDur(pointids)

    with open("2opt830_commonEdges.json") as json_file:
        dict_edges = json.load(json_file)
    starting_node = 174


    #included_nodes = [172, 173, 211, 215, 216, 214, 213, 212, 210, 209, 222, 208, 219, 193, 175, 194, 176, 177, 195, 179, 197, 182, 61, 181, 199, 180, 204, 203, 200, 205, 86, 202, 201, 207]
    #included_nodes = [55, 172, 173, 211, 215, 216, 214, 213, 212, 210, 209, 222, 208, 219, 193, 175, 194, 176, 177, 195, 179, 197, 203, 182, 61, 181, 199, 180, 204, 207, 200, 202, 205, 86, 201]
    included_nodes = [174, 17, 15, 28, 27, 85, 29, 26, 25, 24, 23, 10, 22, 13, 21, 20, 14, 18, 156, 168, 136, 11, 9, 2, 8, 6, 16, 7, 30, 5, 4, 3, 1, 19, 169, 170, 122, 121, 120]
    #included_nodes = [222, 209, 210, 212]
    for node in dict_edges:
        current_list = dict_edges[node]
        new_list = [x for x in current_list if x in included_nodes]
        dict_edges[node] = new_list


elif decision == "T1":
    dur = {1: {4: 1}, 2: {1: 4, 3: 3}, 3: {2: 1}, 4: {2: 2, 3: 2}}
    dist = {1: {2: 3, 3: 3}, 2: {3: 3, 4: 3}, 3: {4: 3}, 4: {2: 3, 3: 3}}

    dict_edges = {
        "1": [4],
        "2": [1, 3],
        "3": [2],
        "4": [2, 3],
    }
    starting_node = 1

elif decision == "T2":
    dur = {1: {2: 5, 3: 2}, 2: {3: 1, 4: 1}, 3: {4: 1}, 4: {2: 1, 3: 1}}
    dist = {1: {2: 3, 3: 3}, 2: {3: 3, 4: 3}, 3: {4: 3}, 4: {2: 3, 3: 3}}
    dict_edges = {
        "1": [2, 3],
        "2": [3, 4],
        "3": [4],
        "4": [2, 3],
    }
    starting_node = 1

#create permutations and save 2 shortest (considering the duration)
tours = all_ways_to_visit_nodes_starting_node(dict_edges, starting_node, dur)

for tour in tours:
    print(tour)
    result_dur = total_duration(tour, dur)
    print(result_dur) #in hours
    result_dist = total_distance(tour, dist)
    print(result_dist) #in km
    result_time = (time.time() - start_time) / 3600
    print("%s seconds" % (result_time)) #in seconds

    #with open("solutions/tour_starting_" + str(starting_node) + ".json" , 'w') as f:
    #    json.dump([tour, result_dur, result_dist, result_time], f)