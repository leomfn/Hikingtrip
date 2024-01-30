import random
from data import *
from algorithms import *
import time
from tour_eval import *
import matplotlib.pyplot as plt

start_time = time.time()

draw = False

# draw a specific tour
if draw:
    tour = [174, 15, 10, 6, 2, 1, 3, 4, 5, 30, 7, 16, 8, 9, 11, 14, 20, 21, 17, 13, 23, 24, 25, 26, 29, 85, 27, 28, 22, 156, 18, 168, 136, 19, 169, 120, 121, 122, 170]
    drawNetworkFromTour(tour, "duration")
    exit()

# find tour with shortest duration/distance
# data: 2 opt using each node as start node and filtered for low duration 
"""with open('start_nodes_1_110.json') as f:
    data = json.load(f)
tour_min(data, "duration")
tour_min(data, "distance")

with open('start_nodes_111_222.json') as f:
    data2 = json.load(f)
tour_min(data2, "duration")
tour_min(data2, "distance")
exit()"""

###
gpx_file = open("data/HWN_2021_11_15.gpx")

gpx = gpxpy.parse(gpx_file)

points = getWayPoints()
pointids = list(points.keys())
dist, dur = getDistAndDur(pointids)

solutions = []
n = 2

# example for defined start and endpoint and randomly shuffled points between

#start_nodes = [i for i in range(1, 111)]
#start_nodes = [i for i in range(109, 111)]
start_nodes = [9]

for start in start_nodes:
    """
    finish = 174
    for i in range(n):
        between = [i for i in range(1, 223)]
        #between = [81, 80, 82, 84, 83, 33, 32, 31, 34, 35, 36, 37, 38, 39, 88, 89, 87, 59, 79, 77, 78, 76, 74, 71, 178, 72, 70, 73, 188, 187, 186, 185, 183, 196, 184, 189, 190, 191, 57, 68, 67, 69, 66, 64, 65, 62, 63, 54, 60, 53, 52, 56, 42, 41, 40, 174]

        random.shuffle(between)
        between.remove(start)
        between.remove(finish)

        tour = [start] + between + [finish]
        #tour = [start] + between
        #tour = between + [finish]

        # 2 opt algorithm
        tour = algorithm("twoOpt", tour, dur)

        if total_duration(tour, dur) < 220:
            solution = {
                'start': start,
                'finish': finish,
                'distance': total_distance(tour, dist),
                'duration': total_duration(tour, dur),
                'tour': tour
            }
            solutions.append(solution)
    print(solutions)
    """


    # ...or n randomized tours without set start and endpoint
    for i in range(n):
        tour = [i for i in range(1, 223)]
    
        random.shuffle(tour)
    
        # 2 opt algorithm
        tour = algorithm("twoOpt", tour, dur)
    
        start = tour[0]
        finish = tour[-1]
    
        if total_distance(tour, dist) < 1200:
            solution = {
                'start': start,
                'finish': finish,
                'distance': total_distance(tour, dist),
                'duration': total_duration(tour, dur),
                'tour': tour
            }
            solutions.append(solution)
            #drawNetworkFromTour(solution["tour"], "duration")

    print(solutions)

with open('2opt_240125.json', 'w') as f:
    json.dump(solutions, f)

print("--- %s seconds ---" % (time.time() - start_time))

# tourEval('2opt.json')
#distributionPlot('2opt830_2.json')

# drawNetwork('2opt.json', "distance")
# drawNetwork('2opt.json', "duration")
