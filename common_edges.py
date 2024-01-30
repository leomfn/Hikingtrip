import json
from tour_eval import *

### use data to find common edges and safe it
with open('2opt830.json') as f:
    data = json.load(f)
#data = [{"start": 2, "tour": [1,2,3,4]}, {"start": 2, "tour": [1,4,2,3]}]
commonEdges = findCommonEdges(data)

with open('2opt830_commonEdges.json', 'w') as f:
    json.dump(commonEdges, f)

### use common edges to change duration matrix
# Opening JSON file with common edges
with open('2opt830_commonEdges.json') as json_file:
    dict_commone_edges = json.load(json_file)

# Opening JSON file with duration
#with open('data/osrm_durations.json') as json_file:
#    matrix_durations = json.load(json_file)

# Print the type of data variable
#print(dict_commone_edges["1"])
#print(matrix_durations[0])