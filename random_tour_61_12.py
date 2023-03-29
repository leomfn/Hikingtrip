import random
import gpxpy
import re
import json
import matplotlib.pyplot as plt

gpx_file = open('HWN_2021_11_15.gpx')

gpx = gpxpy.parse(gpx_file)

points = {}

for i, p in enumerate(gpx.waypoints):
    points[int(re.search(r'\d+', p.name).group(0))] = {
        'name': p.name,
        'lon': p.longitude,
        'lat': p.latitude
    }

pointids = list(points.keys())


def total_distance(tour):
    """returns total distance in km"""
    total_dist = 0
    for i in range(len(tour) - 1):
        total_dist = total_dist + dist[tour[i]][tour[i + 1]]
    return total_dist / 1000


def total_duration(tour):
    """returns total duration in hours"""
    total_dur = 0
    for i in range(len(tour) - 1):
        total_dur = total_dur + dur[tour[i]][tour[i + 1]]
    return total_dur / 60 / 60


with open('osrm_distances.json') as f:
    osrm_dist = json.load(f)

with open('osrm_durations.json') as f:
    osrm_dur = json.load(f)

dist = {}
for i, distlist in enumerate(osrm_dist):
    point_i = pointids[i]
    dist[point_i] = {}
    for j, d in enumerate(distlist):
        point_j = pointids[j]
        dist[point_i][point_j] = d

dur = {}
for i, durlist in enumerate(osrm_dur):
    point_i = pointids[i]
    dur[point_i] = {}
    for j, d in enumerate(durlist):
        point_j = pointids[j]
        dur[point_i][point_j] = d

#
# random.seed(10)

solutions = []

tourpoints = [61, 181, 199, 180, 207, 201, 86, 205, 202, 200, 204, 203, 182, 197, 179, 196, 184, 190, 189, 186, 183,
              185, 187, 73, 70, 72, 178, 71, 188, 74, 76, 78, 77, 79, 87, 59, 80, 81, 82, 84, 83, 33, 32, 31, 34, 35,
              29, 85, 27, 28, 26, 25, 7, 30, 5, 4, 3, 2, 8, 6, 16, 24, 23, 10, 22, 13, 14, 20, 21, 15, 17, 174, 36, 37,
              38, 39, 89, 88, 62, 54, 60, 63, 64, 65, 66, 69, 67, 68, 57, 191, 173, 172, 55, 94, 216, 215, 211, 175,
              194, 176, 177, 195, 193, 219, 208, 222, 209, 210, 212, 213, 214, 198, 100, 218, 98, 99, 92, 95, 93, 96,
              47, 48, 97, 51, 50, 49, 52, 53, 56, 42, 41, 40, 44, 46, 206, 45, 163, 160, 162, 58, 164, 165, 90, 167,
              166, 192, 220, 161, 159, 158, 43, 115, 152, 151, 101, 150, 153, 154, 155, 123, 157, 148, 75, 156, 18, 11,
              9, 168, 136, 19, 1, 169, 170, 122, 121, 120, 118, 117, 116, 119, 124, 126, 125, 112, 91, 114, 108, 111,
              110, 109, 171, 106, 142, 102, 104, 103, 107, 113, 105, 130, 129, 131, 141, 139, 140, 143, 144, 147, 138,
              137, 128, 145, 127, 132, 146, 134, 149, 133, 221, 135, 217, 12]

start = 61
finish = 12

n = 1000

for i in range(n):

    print(f'{round(i / n, 1)} %')

    between = tourpoints[1:221]

    # print('before', between)

    random.shuffle(between)

    # print('after', between)

    tour = [start] + between + [finish]
    # print('tour', tour)

    # 2 opt algorithm

    improvement = True
    runs = 0
    while improvement:
        # print('run', runs)
        improvement = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour) - 1):
                dist_original = dist[tour[i - 1]][tour[i]] + \
                                dist[tour[j]][tour[j + 1]]
                dist_test = dist[tour[i - 1]][tour[j]] + dist[tour[i]][tour[j + 1]]
                if dist_test < dist_original:
                    tour[i:j + 1] = reversed(tour[i:j + 1])
                    improvement = True
        runs += 1

    solution = {
        'start': start,
        'finish': finish,
        'distance': total_distance(tour),
        'duration': total_duration(tour),
        'tour': tour
    }

    solutions.append(solution)

with open('2opt.json', 'w') as f:
    json.dump(solutions, f)