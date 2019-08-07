import utils
import pandas as pd
from numpy import NaN
file = utils.parse_excel("responses.xlsx")
types = utils.parse_config("config_file.txt")
grouped = {}
for i, qn in enumerate(file.keys()):
    if types[i] not in grouped.keys():
        grouped[types[i]] = [qn]
    else:
        grouped[types[i]].append(qn)
max_len = max(len(value) for value in grouped.values())
for qntype, qns in grouped.items():
    for i in range(max_len - len(qns)):
        grouped[qntype].append(NaN)
df = pd.DataFrame(grouped)
print(df)
