import pandas as pd
import json


save_path = "tables/data_info.xlsx"

df = pd.read_excel("tables/data_info_raw.xlsx")
relations = {
    r : 0
    for r in df['relation']
}
# print(relations)

with open("search/pile/merge.json", 'r') as f:
    data = json.load(f)

for i in range(len(data)):
    relations[data[i]['rel']] += 1
# print(relations)

for i in range(len(df)):
    for k in relations.keys():
        if k==df.loc[i, 'relation']:
            df.loc[i, 'amounts'] = relations[k]

print(len(data))
print(sum(list(relations.values())))

df.to_excel(save_path)