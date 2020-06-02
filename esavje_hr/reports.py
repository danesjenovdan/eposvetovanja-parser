import pandas as pd
import sys
import os
import glob

files = glob.glob("out\\reports\\*.csv")

# writer = pd.ExcelWriter('out\\reports.xlsx')
# for csvfilename in files:
#   sheet_name = os.path.splitext(csvfilename)[0].split('-')[-1]
#   print(sheet_name)
#   df = pd.read_csv(csvfilename)
#   df.to_excel(writer, sheet_name=sheet_name)
# writer.save()


li = []
for filename in files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)
frame = pd.concat(li, axis=0, ignore_index=True)
writer = pd.ExcelWriter('out\\reports_all.xlsx')
frame.to_excel(writer, sheet_name='all')
writer.save()
