import json
from possible_ways import *
from data import *


#load duration matrix

"""points = getWayPoints()
pointids = list(points.keys())
dist, dur = getDistAndDur(pointids)
print(dur)"""

dur = {1: {4: 1}, 2: {1: 4, 3: 3}, 3: {2: 1}, 4: {2: 2, 3: 2}}

#load dictionary with edges (5 nearest or determined by previous runs
"""with open("2opt830_commonEdges.json") as json_file:
    dict_edges = json.load(json_file)
print(dict_edges)"""

dict_edges = {
    1: [4],
    2: [1, 3],
    3: [2],
    4: [2, 3],
}

#create permutations and save 2 shortest (considering the duration)

starting_node = 1
tours = all_ways_to_visit_nodes_starting_node(dict_edges, starting_node, dur)

for tour in tours:
    print(tour)
    result_dur = total_duration(tour, dur)
    print(result_dur * 3600)

#print duration and distance