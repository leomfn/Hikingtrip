import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_json('opt_distance_shuffleall.json')

# print(df.head())

print(df.sort_values('duration'))

print(df['duration'].min())

# df.boxplot('distance')

df.hist('duration')

plt.show()