import random
from data import *
from algorithms import *
import time
from tour_eval import *
import matplotlib.pyplot as plt

eval = True

if eval:
    ### draw a specific tour
    tour = [174, 15, 10, 6, 2, 1, 3, 4, 5, 30, 7, 16, 8, 9, 11, 14, 20, 21, 17, 13, 23, 24, 25, 26, 29, 85, 27, 28, 22, 156, 18, 168, 136, 19, 169, 120, 121, 122, 170]


    drawNetworkFromTour(tour, "duration")
    exit()

"""with open('start_nodes_1_110.json') as f:
    data = json.load(f)
tourMin(data, "duration")
tourMin(data, "distance")

with open('start_nodes_111_222.json') as f:
    data2 = json.load(f)
tourMin(data2, "duration")
tourMin(data2, "distance")
exit()"""

### use data to find common edges and safe it
"""with open('2opt830.json') as f:
    data = json.load(f)
#data = [{"start": 2, "tour": [1,2,3,4]}, {"start": 2, "tour": [1,4,2,3]}]
commonEdges = findCommonEdges(data)

with open('2opt830_commonEdges.json', 'w') as f:
    json.dump(commonEdges, f)
exit()"""

"""### use common edges to change duration matrix
# Opening JSON file with common edges
with open('2opt830_commonEdges.json') as json_file:
    dict_commone_edges = json.load(json_file)

# Opening JSON file with duration
with open('data/osrm_durations.json') as json_file:
    matrix_durations = json.load(json_file)

# Print the type of data variable
#print(dict_commone_edges["1"])
#print(matrix_durations[0])"""

###
start_time = time.time()

gpx_file = open("data/HWN_2021_11_15.gpx")

gpx = gpxpy.parse(gpx_file)

points = getWayPoints()
pointids = list(points.keys())
dist, dur = getDistAndDur(pointids)

solutions = []
n = 100000
last = 0

# example for defined start and endpoint and randomly shuffled points between

#start_nodes = [i for i in range(1, 111)]
#start_nodes = [i for i in range(109, 111)]
start_nodes = [55]
print(start_nodes)
for start in start_nodes:
    print(start)
    #start = 9
    finish = 174
    for i in range(n):
        number = (int(round(i / n, 3) * 100))
        if (number % 10 == 0) & (number != last):
            last = number
            print(f'{number} %')

        #between = [i for i in range(1, 223)]
        between = [81, 80, 82, 84, 83, 33, 32, 31, 34, 35, 36, 37, 38, 39, 88, 89, 87, 59, 79, 77, 78, 76, 74, 71, 178, 72, 70, 73, 188, 187, 186, 185, 183, 196, 184, 189, 190, 191, 57, 68, 67, 69, 66, 64, 65, 62, 63, 54, 60, 53, 52, 56, 42, 41, 40, 174]

        random.shuffle(between)
        #between.remove(start)
        between.remove(finish)

        #tour = [start] + between + [finish]
        #tour = [start] + between
        tour = between + [finish]

        # 2 opt algorithm

        tour = algorithm("twoOpt", tour, dur)

        start = tour[0]
        finish = tour[-1]

        if total_duration(tour, dur) < 33.1:
            solution = {
                'start': start,
                'finish': finish,
                'distance': total_distance(tour, dist),
                'duration': total_duration(tour, dur),
                'tour': tour
            }
            solutions.append(solution)
            print(solution)

    # ...or n randomized tours without set start and endpoint
    """
    for i in range(n):
        tour = [i for i in range(1, 223)]
    
        number = (int(round(i / n, 3) * 100))
        if (number % 10 == 0) & (number != last):
            last = number
            print(f'{number} %')
    
        random.shuffle(tour)
    
        # 2 opt algorithm
    
        tour = algorithm("twoOpt", tour, dur)
    
        start = tour[0]
        finish = tour[-1]
    
        if total_distance(tour, dur) < 200:
            solution = {
                'start': start,
                'finish': finish,
                'distance': total_distance(tour, dist),
                'duration': total_duration(tour, dur),
                'tour': tour
            }
            solutions.append(solution)"""

    print(start)
    print(solutions)

"""with open('start_nodes_1_222.json', 'w') as f:
    json.dump(solutions, f)"""

# tourEval('2opt.json')
print("--- %s hours ---" % ((time.time() - start_time) / 60))
#distributionPlot('2opt830_2.json')

# drawNetwork('2opt.json', "distance")
# drawNetwork('2opt.json', "duration")
