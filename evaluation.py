import json
import pandas as pd

# with open('opt_distance_solutions.json', 'r') as f:
#   data = json.load(f)
  
# print(len(data))

df = pd.read_json('opt_distance_solutions.json')

print(df.shape)
print(df.head())

print('sort by distance')
df_distance = df.sort_values('distance')
print(df_distance.head())
df_distance.iloc[0, :].to_json('shortest_distance_tour.json')

print('sort by duration')
df_duration = df.sort_values('duration')
print(df_duration.head)

