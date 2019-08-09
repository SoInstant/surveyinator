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
encoded = {}
for datatype,qns in grouped.items():
    temp_enc = utils.Encoder(qns)
    encoded[datatype] = temp_enc.embeddings
max_len = max(len(value) for value in encoded.values())
for qntype, qns in encoded.items():
    for i in range(max_len - len(qns)):
        encoded[qntype].append(NaN)
df = pd.DataFrame(encoded)
print(df)
