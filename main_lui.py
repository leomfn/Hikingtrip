import random
from data import *
from algorithms import *
import time
from tour_eval import *
import matplotlib.pyplot as plt

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

# example for defined start and endpoint and randomly shuffled points between
"""tourpoints = [61,181,199,180,207,201,86,205,202,200,204,203,182,197,179,196,184,190,189,186,183,185,187,73,70,72,178,71,188,74,76,78,77,79,87,59,80,81,82,84,83,33,32,31,34,35,29,85,27,28,26,25,7,30,5,4,3,2,8,6,16,24,23,10,22,13,14,20,21,15,17,174,36,37,38,39,89,88,62,54,60,63,64,65,66,69,67,68,57,191,173,172,55,94,216,215,211,175,194,176,177,195,193,219,208,222,209,210,212,213,214,198,100,218,98,99,92,95,93,96,47,48,97,51,50,49,52,53,56,42,41,40,44,46,206,45,163,160,162,58,164,165,90,167,166,192,220,161,159,158,43,115,152,151,101,150,153,154,155,123,157,148,75,156,18,11,9,168,136,19,1,169,170,122,121,120,118,117,116,119,124,126,125,112,91,114,108,111,110,109,171,106,142,102,104,103,107,113,105,130,129,131,141,139,140,143,144,147,138,137,128,145,127,132,146,134,149,133,221,135,217,12]
start = 61
finish = 12

n = 1000

for i in range(n):
    print(f'{round(i / n, 1)} %')

    between = tourpoints[1:221]
    random.shuffle(between)
    
    tour = [start] + between + [finish]
    """

# ...or n randomized tours without set start and endpoint
n = 1000000
last = 0
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

    if total_distance(tour, dur) < 170:
        solution = {
            'start': start,
            'finish': finish,
            'distance': total_distance(tour, dist),
            'duration': total_duration(tour, dur),
            'tour': tour
        }
        solutions.append(solution)

with open('2opt830_dur.json', 'w') as f:
    json.dump(solutions, f)

# tourEval('2opt.json')
print("--- %s hours ---" % ((time.time() - start_time) / 3600))
#distributionPlot('2opt830_2.json')

# drawNetwork('2opt.json', "distance")
# drawNetwork('2opt.json', "duration")
