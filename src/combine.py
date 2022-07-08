import pandas as pd
import sys
import os

in_dir = sys.argv[1]
out_file = sys.argv[2]

sort_col = sys.argv[3] if len(sys.argv) > 3 else None

dfs = []
for csv_file in os.listdir(in_dir):
    dfs.append(pd.read_csv(in_dir + csv_file))

combined = pd.concat(dfs,ignore_index=True)

if sort_col is not None:
    combined.sort_values(sort_col,inplace=True)

combined.to_csv(out_file,index=False)