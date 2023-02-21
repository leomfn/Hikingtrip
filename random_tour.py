import random
import gpxpy
import re
import json

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


n = 1000

for i in range(n):
  tour = [i for i in range(1, 223)]

  print(f'{round(i/n, 3)*100} %')
  



  # print('before', between)

  random.shuffle(tour)
#   if i < 15:
#     print(tour[:15])
  
  start = tour[0]
  finish = tour[-1]


  # print('after', between)

  # print('tour', tour)
    
    
  # 2 opt algorithm

  improvement = True
  runs = 0
  while improvement:
      # print('run', runs)
      improvement = False
      for i in range(1, len(tour)-2):
          for j in range(i+1, len(tour)-1):
              dist_original = dist[tour[i-1]][tour[i]] + \
                  dist[tour[j]][tour[j+1]]
              dist_test = dist[tour[i-1]][tour[j]] + dist[tour[i]][tour[j+1]]
              if dist_test < dist_original:
                  tour[i:j+1] = reversed(tour[i:j+1])
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
  
with open('opt_distance_shuffleall.json', 'w') as f:
    json.dump(solutions, f)