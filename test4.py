from copy import copy

from data import *
from tour_eval import *
from algorithms import *
import random


### test4 = solve path for interesting region
# 120 and 135 are missing and added after random shuffling
# 120 and 135 are set for start and finish
points = getWayPoints()
pointids = list(points.keys())
pointidsRegion = [116, 117, 118, 119, 108, 114, 91, 111, 110, 109, 171, 106, 142, 102, 104, 103, 107, 113, 112, 125, 124, 126, 105, 130, 129, 131, 141, 139, 140, 143, 144, 147, 146, 138, 137, 128, 145, 127, 132, 134, 149, 133, 221]
dist, dur = getDistAndDur(pointids)

solutions = []

# ...or n randomized tours without set start and endpoint
n = 10000
last = 0
for i in range(n):
    tour = copy(pointidsRegion)

    number = (int(round(i / n, 3) * 100))
    if (number % 10 == 0) & (number != last):
        last = number
        print(f'{number} %')

    random.shuffle(tour)
    tour.insert(0, 120)
    tour.append(135)

    # 2 opt algorithm
    tour = algorithm("twoOpt", tour, dist)
    start = tour[0]
    finish = tour[-1]

    if total_distance(tour, dist) < 300:
        solution = {
            'start': start,
            'finish': finish,
            'distance': total_distance(tour, dist),
            'duration': total_duration(tour, dur),
            'tour': tour
        }
        solutions.append(solution)

with open('2opt830_interestingRegion1.json', 'w') as f:
    json.dump(solutions, f)

duplicateTours(solutions)

tourmin = tourMin(solutions, "duration")
drawNetworkFromTour(tourmin, "duration")