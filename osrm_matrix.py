import requests
import re
import json
import gpxpy

gpx_file = open('/Users/Lui/Documents/Semester6/Bachelorarbeit/HWN_2021_11_15.gpx')

gpx = gpxpy.parse(gpx_file)

points = {}

for i, p in enumerate(gpx.waypoints):
    points[int(re.search(r'\d+', p.name).group(0))] = {
        'name': p.name,
        'lon': p.longitude,
        'lat': p.latitude
    }

# print(points)

base_url = "http://router.project-osrm.org/table/v1/foot/"

url_extension = ';'.join([','.join([str(value['lon']), str(value['lat'])]) for key, value in points.items()])

#r = requests.get(base_url + url_extension + '?' + 'annotations=duration,distance')

r = requests.get('http://router.project-osrm.org/table/v1/foot/'
                     '13.388860,52.517037;13.397634,52.529407;13.428555,52.523219?annotations=distance,duration')


print('status', r.status_code)

# print(r.json().keys())

print('durations') # seconds
print(r.json()['durations'])

print('distances') # meters
print(r.json()['distances'])

#with open('data/osrm_distances.json', 'w') as f:
#  json.dump(r.json()['distances'], f, indent=2)

#with open('data/osrm_durations.json', 'w') as f:
#  json.dump(r.json()['durations'], f, indent=2)