import pandas as pd
from io import StringIO
import json
import xobjects as xo

fname = 'sler_1705_60_06_cw50_4b.twiss'

with open(fname, 'r') as f:
    content = f.read()

lines = content.split('\n')
header = lines[0]

content = '\n'.join(ll for ll in lines if 's(m)' not in ll)

# prepend header
content = header + '\n' + content

df = pd.read_csv(StringIO(content), delim_whitespace=True)

out_dict = {}
for nn in df.columns:
    out_dict[nn] = list(df[nn].values)

with open(fname+'.json', 'w') as fid:
    json.dump(out_dict, fid, cls=xo.JEncoder)