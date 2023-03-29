import json
from itertools import chain
from tour_eval import *

# read the input file
import pandas as pd

with open('2opt830.json') as f:
    data = json.load(f)

print("There are {} solutions.".format(len(data)))

# checks for duplicates
duplicateTours(data)

# draws network
#drawNetwork(data, "distance")

# analyzes which edges are most common
analyzeEdges(data, 1000)
