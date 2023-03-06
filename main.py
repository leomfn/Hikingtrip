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

# print(points)

if len(points) != len(set(points.keys())):
    raise Exception('Point IDs are not unique')

with open('data/osrm_distances.json') as f:
    osrm_dist = json.load(f)

with open('data/osrm_durations.json') as f:
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


point_combinations = [(i, j) for i in pointids for j in pointids]

solutions = []

for i in range(len(point_combinations)):
    print(f'combination {i}/{len(point_combinations)}')

    start = point_combinations[i][0]
    finish = point_combinations[i][1]
    residue = list(filter(lambda p: p not in [start, finish], pointids))

    # print(start, finish)

    tour = [start] + residue + [finish]

    # print(tour)

    # fig, ax = plt.subplots()
    # fig.suptitle(f'From HWN{start:03d} (green) to HWN{finish:03d} (red)')

    # # start piont
    # ax.scatter(
    #     x=points[start]['lon'],
    #     y=points[start]['lat'],
    #     c='lightgreen',
    #     s=100,
    #     alpha=0.5
    # )

    # # end point
    # ax.scatter(
    #     x=points[finish]['lon'],
    #     y=points[finish]['lat'],
    #     c='tomato',
    #     s=100,
    #     alpha=0.5
    # )
    # ax.scatter(
    #     x=[points[p]['lon'] for p in points.keys()],
    #     y=[points[p]['lat'] for p in points.keys()],
    #     c='black',
    #     s=10
    # )

    # lines, = ax.plot(
    #     [points[p]['lon'] for p in tour],
    #     [points[p]['lat'] for p in tour],
    #     '-',
    #     alpha=0.5
    # )

    improvement = True
    runs = 0
    while improvement:
        print('run', runs)
        improvement = False
        for i in range(1, len(tour)-2):
            for j in range(i+1, len(tour)-1):
                dist_original = dist[tour[i-1]][tour[i]] + \
                    dist[tour[j]][tour[j+1]]
                dist_test = dist[tour[i-1]][tour[j]] + dist[tour[i]][tour[j+1]]
                if dist_test < dist_original:
                    tour[i:j+1] = reversed(tour[i:j+1])

                    # lines.set_data(
                    #     [points[p]['lon'] for p in tour],
                    #     [points[p]['lat'] for p in tour]
                    # )
                    # ax.set_title(
                    #     f'total distance: {round(total_distance(tour), 1)} km total duration: {round(total_duration(tour), 1)} h'
                    # )
                    # plt.pause(0.0001)

                    improvement = True
        runs += 1
    
    # plt.savefig(f'images/opt_distance/opt_distance_{start:03d}_{finish:03d}')

    print('finished optimization')
    # plt.show()
    # plt.pause(1)

    solution = {
        'start': start,
        'finish': finish,
        'distance': total_distance(tour),
        'duration': total_duration(tour),
        'tour': tour
    }

    solutions.append(solution)

with open('opt_distance_solutions.json', 'w') as f:
    json.dump(solutions, f)
