import random
from data import *
from algorithms import *
import time
from tour_eval import *
import matplotlib.pyplot as plt

### draw a specific tour
"""tour =  [9, 11, 136, 19, 168, 156, 18, 14, 20, 21, 13, 15, 17, 174, 40, 41, 42, 56, 52, 53, 60, 54, 63, 62, 64, 69, 66, 65, 74, 76, 78, 77, 79, 59, 80, 81, 82, 84, 83, 33, 32, 31, 35, 34, 37, 87, 89, 88, 38, 39, 36, 29, 85, 27, 28, 26, 25, 24, 16, 23, 10, 22, 8, 6, 7, 30, 5, 4, 3, 2, 1, 169, 170, 122, 121, 120, 118, 117, 119, 116, 108, 114, 91, 111, 110, 109, 171, 106, 142, 102, 104, 103, 107, 112, 125, 124, 126, 113, 105, 130, 129, 131, 141, 139, 140, 143, 144, 147, 145, 127, 128, 137, 138, 146, 134, 132, 149, 133, 221, 135, 217, 12, 75, 148, 123, 155, 154, 153, 150, 101, 151, 152, 115, 43, 158, 161, 220, 192, 166, 167, 90, 165, 164, 162, 159, 157, 163, 160, 58, 45, 206, 46, 44, 49, 50, 51, 97, 48, 47, 96, 95, 93, 92, 99, 98, 218, 100, 198, 214, 213, 212, 210, 209, 222, 208, 219, 193, 176, 194, 175, 211, 215, 216, 94, 55, 172, 173, 191, 57, 67, 68, 70, 72, 178, 71, 73, 187, 188, 185, 183, 186, 189, 190, 184, 196, 195, 177, 179, 197, 182, 61, 181, 199, 180, 204, 203, 200, 205, 86, 202, 201, 207]

drawNetworkFromTour(tour, "duration")
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
n = 50000
last = 0

# example for defined start and endpoint and randomly shuffled points between

start_nodes = [i for i in range(1, 111)]
#start_nodes = [i for i in range(111, 223)]
print(start_nodes)
for start in start_nodes:
    print(start)
    #start = 9
    #finish = 120
    for i in range(n):
        number = (int(round(i / n, 3) * 100))
        if (number % 10 == 0) & (number != last):
            last = number
            print(f'{number} %')

        between = [i for i in range(1, 223)]
        #between = [81, 120, 121,122, 169, 170, 1, 19, 136, 9, 11, 22, 10, 23, 24, 16, 6, 8, 2, 3, 4, 5, 30, 7, 25, 26, 28, 27, 85, 29, 35, 34, 32, 31, 33, 83, 84, 82, 80, 81, 120]

        random.shuffle(between)
        between.remove(start)
        #between.remove(finish)

        #tour = [start] + between + [finish]
        tour = [start] + between

        # 2 opt algorithm

        tour = algorithm("twoOpt", tour, dur)

        start = tour[0]
        finish = tour[-1]

        if total_duration(tour, dur) < 171:
            solution = {
                'start': start,
                'finish': finish,
                'distance': total_distance(tour, dist),
                'duration': total_duration(tour, dur),
                'tour': tour
            }
            solutions.append(solution)

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

with open('start_nodes_1_110.json', 'w') as f:
    json.dump(solutions, f)

# tourEval('2opt.json')
print("--- %s hours ---" % ((time.time() - start_time) / 60))
#distributionPlot('2opt830_2.json')

# drawNetwork('2opt.json', "distance")
# drawNetwork('2opt.json', "duration")
