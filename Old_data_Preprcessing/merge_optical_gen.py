import pandas as pd
import numpy as np

round1 = pd.read_csv("C:\Team3\Data\OIBC2023_data\optical_gen_round1.csv")
round1['round'] = 1
round1 = round1[['time', 'round', 'amount']]


print(round1)

round2 = pd.read_csv("C:\Team3\Data\OIBC2023_data\optical_gen_round2.csv")
round2['round'] = 2
round2 = round2[['time', 'round', 'amount']]

print(round2)
result = pd.concat([round1, round2])  # Correct the concatenation
print(result)




#11618

result.to_csv("C:\Team3\Data\OIBC2023_data\optical_gen_merged.csv", mode='w', index=False)
