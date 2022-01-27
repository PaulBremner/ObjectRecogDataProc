#! "C:\Users\p2-bremner\AppData\Local\Programs\Python\Python39\python.exe"

import glob
import pkg_resources
#pkg_resources.require("pandas==1.0.5")
pkg_resources.require("numpy==1.20.3")
import pandas as pd
import os
import csv
#import pingouin as pg
import sys
import numpy as np
import json

print(sys.executable)
print("PD " + pd.__version__)
print("NP " + np.__version__)

#exit()
csvfiles = glob.glob('*.csv')
data = {}
i = 0
#print(csvfiles)
#exit()
c = os.path.basename(csvfiles[0]).split('.')[0]
renderold = c[:len(c)-2]
lenold = len(pd.read_csv(csvfiles[0]).PID)
for csvfile in csvfiles:
    c = os.path.basename(csvfile).split('.')[0]
    data[c] = pd.read_csv(csvfile)

    if c[:len(c)-2] != renderold:
        i += lenold
        renderold = c[:len(c)-2]
        lenold = len(data[c].PID)

    for j in range(len(data[c].PID)):
        data[c].loc[j, 'PID'] = data[c].PID[j] + i

    #if i < 80:
    #    print(data[c].PID)
#exit()
#print(data.keys())
objectresults = {}
anovainput = {'PID': [], 'object': [], 'colour': [], 'motion': [], 'render': []}

for key in data.keys():
    objectresults[key] = [data[key].mean().object]
    #objectresults[key].append(data[key].std().object)
    anovainput['PID'] += list(data[key].PID)
    anovainput['object'] += list(data[key].object)
    anovainput['colour'] += [key[-2]]*len(data[key].object)
    anovainput['motion'] += [key[-1]]*len(data[key].object)
    anovainput['render'] += [key[:len(key)-2]]*len(data[key].object)
#print(objectresults)
#exit()
#anovainput = {'object':[0.1,0.2,0.3,0.4]}#, 'colour': anovainput['colour']}
#df = pd.DataFrame.from_dict(anovainput)#, dtype={'colour': str, 'motion': str, 'render': str})
#df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=['a', 'b', 'c'])
#print(df.dtypes)
#exit()
#print(df.head())
#exit()
#pg.mixed_anova(data=df, dv='object', between='render', within="motion")
#store_export = pd.HDFStore("recog_res_3wayMixed.h5")
#store_export.append("df", df, data_columns=df.columns)
#store_export
#dfjson = df.to_json()#todo dataframe to json no good as incorrectly assigns PIDs based on row number, each participant will have 4 rows
#with open("recog_res_3wayMixed.json", 'w') as jsonf:
#    jsonf.write(dfjson)
with open('response_data/anovainput.json', 'w') as f:
    json.dump(anovainput, f)

exit()

csv_file = 'objectresults.csv'

with open(csv_file, 'w', newline='', encoding='utf-8') as f:  # You will need 'wb' mode in Python 2.x
    w = csv.DictWriter(f, objectresults.keys())
    w.writeheader()
    w.writerow(objectresults)