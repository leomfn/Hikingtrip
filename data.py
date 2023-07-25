import json
import re
import gpxpy


def getWayPoints():
    gpx_file = open("/Users/Lui/Documents/Semester6/Bachelorarbeit/HWN_2021_11_15.gpx")

    gpx = gpxpy.parse(gpx_file)

    points = {}

    for i, p in enumerate(gpx.waypoints):
        points[int(re.search(r'\d+', p.name).group(0))] = {
            'name': p.name,
            'lon': p.longitude,
            'lat': p.latitude
        }

    return points

def getDistAndDur(pointids):
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

    return dist, dur

def total_distance(tour, dist):
    """returns total distance in km"""
    total_dist = 0
    for i in range(len(tour) - 1):
        total_dist = total_dist + dist[tour[i]][tour[i + 1]]
    return total_dist / 1000

def total_duration(tour, dur):
    """returns total duration in hours"""
    total_dur = 0
    for i in range(len(tour) - 1):
        total_dur = total_dur + dur[tour[i]][tour[i + 1]]
    return total_dur / 60 / 60

