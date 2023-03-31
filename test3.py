import random
import gpxpy
import random
from algorithms import *
from tour_eval import *

### test3.py = set some edges, create new tour, analyze it

gpx_file = open("/Users/Lui/Documents/Semester 6/Bachelorarbeit/HWN_2021_11_15.gpx")

gpx = gpxpy.parse(gpx_file)

points = getWayPoints()
pointids = list(points.keys())
dist, dur = getDistAndDur(pointids)

def createTourDefPair():
    # Specify pairs in a dictionary where key is the number that needs to be followed by its pair
    edges = {122: 170, 170: 122,
             31: 32, 32: 31,
             199: 180, 180: 199,
             86: 205, 205: 86,
             210: 212, 212: 210,
             #212: 213, 213: 212,
             166: 192, 192: 166,
             88: 89, 89: 88,
             20: 14, 14: 20,
             151: 101, 101: 151,
             117: 118, 118: 117,
             104: 103, 103: 104,
             130: 129, 129: 130,
             131: 141, 141: 131}

    # Create a list of randomly shuffled numbers between 1 and 222
    tour = list(range(1, 223))
    random.shuffle(tour)

    for point in tour:
        if point in edges:
            #print("poin: {}".format(point))
            idx = tour.index(point)
            #print("idx: {}".format(idx))
            tour.remove(edges[point])
            #print(tour)
            tour.insert(idx+1, edges[point])
            del edges[edges[point]]
            #print(tour)
            #print(edges)

    return tour

tour = createTourDefPair()

tour = algorithm("twoOpt", tour, dist)

print(tour)
print(total_distance(tour, dist))
print(total_duration(tour, dur))
drawNetworkFromTour(tour, "distance")