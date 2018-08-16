from sqlalchemy import create_engine
import tushare as ts
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import requests
import time

# get convertibles from tushare (which retrieves from stockstar.com)
engine = create_engine('sqlite:///C:\\D\\sqlite3\\tradingsystem.db')
df = ts.new_cbonds(default=0)
df.to_sql('bond_convertibles',engine,if_exists='replace',chunksize=10)
tdf = pd.read_sql('bond_convertibles',engine)   # tushare df

# get convertibles from jisilu
jisiluUrl = 'https://www.jisilu.cn/data/cbnew/cb_list/?___jsl=LST___t='+str(time.time())
resp = requests.get(url=jisiluUrl)
data = resp.json()
cbonds=[]
for r in data['rows']:
    cbonds.append(r['cell'])
jdf = pd.DataFrame.from_dict(cbonds)        # jisilu df
jdf.bond_id = jdf.bond_id.astype(np.int64)

# compare tushare with jisilu
# missedInTushare = jdf[~jdf.bond_id.isin(tdf.bcode)][['bond_id','bond_nm']]

# get end of day history pricing data
allConvertibles = pd.merge(tdf[['bcode']].rename(columns={'bcode':'bond_id'}), jdf[['bond_id']],how='outer',on='bond_id')
for index, row in allConvertibles.iterrows():
    histDf = ts.get_hist_data(str(row['bond_id']))
    if histDf is None:
        print("no end of day history data for "+ str(row['bond_id']))
    else:
        histDf['bond_id'] = row['bond_id']
        histDf.set_index(['bond_id'],append=True,inplace=True)
        print(histDf)
        histDf.to_sql('bond_convertibles_eodHist',engine,if_exists='replace',chunksize=10)
        
