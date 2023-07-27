import json
from possible_ways import *
from data import *
import time


#start time measurement
start_time = time.time()

#load duration and distance matrix
#load dictionary with edges (5 nearest or determined by previous runs

decision = "T1"

if decision == "R":
    points = getWayPoints()
    pointids = list(points.keys())
    dist, dur = getDistAndDur(pointids)

    with open("2opt830_commonEdges.json") as json_file:
        dict_edges = json.load(json_file)
    starting_node = 81

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

    with open("solutions/tour_starting_" + str(starting_node) + ".json" , 'w') as f:
        json.dump([tour, result_dur, result_dist, result_time], f)