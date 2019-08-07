import utils
import pandas as pd
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
    if len(qns) != max_len:
        for i in range(max_len - len(qns)):
            grouped[qntype].append("")
df = pd.DataFrame(grouped)
