from copy import copy

from data import *
from tour_eval import *
from algorithms import *
import random


### solve path for interesting region
# 120 and 135 are missing and added after random shuffling
# 120 and 135 are set for start and finish
points = getWayPoints()
pointids = list(points.keys())
pointidsRegion1 = [116, 117, 118, 119, 108, 114, 91, 111, 110, 109, 171, 106, 142, 102, 104, 103, 107, 113, 112, 125, 124, 126, 105, 130, 129, 131, 141, 139, 140, 143, 144, 147, 146, 138, 137, 128, 145, 127, 132, 134, 149, 133, 221]
pointidsRegion = [217, 168, 12, 75, 148, 156, 18, 14, 20, 21, 13, 15, 17, 174, 40, 41, 42, 39, 36, 37, 38, 88, 89, 87, 59, 79, 77, 78, 76, 74, 71, 178, 72, 70, 73, 187, 188, 185, 183, 186, 189, 190, 184, 196, 195, 177, 176, 194, 175, 211, 215, 216, 94, 55, 172, 173, 191, 57, 68, 67, 69, 66, 64, 65, 62, 63, 60, 54, 53, 56, 52, 49, 44, 46, 206, 45, 90, 165, 164, 58, 163, 160, 162, 161, 158, 159, 157, 123, 155, 154, 153, 150, 101, 151, 152, 115, 43, 220, 192, 166, 167, 96, 48, 47, 50, 51, 97, 93, 95, 92, 99, 98, 218, 100, 198, 214, 213, 212, 210, 209, 222, 208, 219, 193, 179, 197, 182, 61, 181, 199, 180, 207, 204, 203, 200, 202, 201, 86]
dist, dur = getDistAndDur(pointids)

solutions = []

# ...or n randomized tours without set start and endpoint
n = 1000
last = 0
for i in range(n):
    tour = copy(pointidsRegion)

    number = (int(round(i / n, 3) * 100))
    if (number % 10 == 0) & (number != last):
        last = number
        print(f'{number} %')

    random.shuffle(tour)
    tour.insert(0, 135)
    tour.append(205)

    # 2 opt algorithm
    tour = algorithm("twoOpt", tour, dist)
    start = tour[0]
    finish = tour[-1]

    if total_distance(tour, dist) < 534:
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
tourmin = tourMin(solutions, "distance")
#drawNetworkFromTour(tourmin, "duration")
drawNetworkFromTour(tourmin, "distance")