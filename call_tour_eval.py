import json
from itertools import chain
from tour_eval import *

# read the input file
import pandas as pd

with open('2opt830.json') as f:
    data = json.load(f)

print("There are {} solutions.".format(len(data)))

#checks for duplicates
duplicateTours(data)

#tourMin(data, "distance")
tour_min(data, "duration")

#draws network
drawNetwork(data, "duration")

#analyzes which edges are most common
analyzeEdges(data, 50)

"""df = pd.DataFrame(data)
df = df.loc[df["distance"] < 820]

for tour in df["tour"]:
    drawNetworkFromTour(tour, "distance")

print(df.loc[df["distance"] < 820])"""