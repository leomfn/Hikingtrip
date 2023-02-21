import matplotlib.pyplot as plt
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

with open('shortest_distance_tour.json') as f:
  tourdata = json.load(f)
  
print(tourdata)

tour = tourdata['tour']
start = tour[0]
finish = tour[-1]
# tour = tour[1:-1]

fig, ax = plt.subplots()
fig.suptitle(f'From HWN{start:03d} (green) to HWN{finish:03d} (red)')

lines, = ax.plot(
    [points[p]['lon'] for p in tour],
    [points[p]['lat'] for p in tour],
    '-',
    alpha=0.5
)

ax.scatter(
    x=[points[p]['lon'] for p in points.keys()],
    y=[points[p]['lat'] for p in points.keys()],
    c='black',
    s=10
)

# start piont
ax.scatter(
    x=points[start]['lon'],
    y=points[start]['lat'],
    c='lightgreen',
    s=100
)

# end point
ax.scatter(
    x=points[finish]['lon'],
    y=points[finish]['lat'],
    c='tomato',
    s=100
)

plt.savefig('shortest_distance_tour.png')