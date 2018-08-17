from sqlalchemy import create_engine
import tushare as ts
import pandas as pd
#import numpy as np
import requests
import time
import json

# load configurations
with open('config.json') as config_file:  
    config = json.load(config_file)
# create db engine
engine = create_engine(config['convertibles']['dbConnString'])

# get convertibles from tushare (which retrieves from stockstar.com)
tdf = ts.new_cbonds(default=0)   # tushare df
tdf.rename(columns={'bcode':'bond_id'},inplace=True)
tdf.bond_id = tdf.bond_id.astype(str) 
#TODO: design a normalized table schema so that data from difference sources can be merged.
#TODO: create table before hand instead of runtime creation, use mysql "Using INSERT ... ON DUPLICATE KEY UPDATE" to have better control than to_sql 
tdf.set_index(['bond_id']).to_sql(config['convertibles']['tblConvertibleReference'],engine,if_exists='append',chunksize=10)

# get convertibles from jisilu
jisiluUrl = config['convertibles']['jisiluUrlBase']+str(time.time())
resp = requests.get(url=jisiluUrl)
data = resp.json()
cbonds=[]
for r in data['rows']:
    cbonds.append(r['cell'])
jdf = pd.DataFrame.from_dict(cbonds)        # jisilu df
#jdf.bond_id = jdf.bond_id.astype(np.int64) 
jdf.bond_id = jdf.bond_id.astype(str) 

# compare tushare with jisilu
missedInTushare = jdf[~jdf.bond_id.isin(tdf.bond_id)][['bond_id','bond_nm']]

# get end of day history pricing data
allConvertibles = pd.merge(tdf[['bond_id']], jdf[['bond_id']],how='outer',on='bond_id')
for index, row in allConvertibles.iterrows():
    histDf = ts.get_k_data(str(row['bond_id']))
    if histDf is None or histDf.empty:
        print("no end of day history data for "+ str(row['bond_id']))
    else:
        histDf['bond_id'] = row['bond_id']
        histDf.set_index(['bond_id','date'],inplace=True)
        histDf.to_sql(config['convertibles']['tblConvertibleEODHistory'],engine,if_exists='append',chunksize=10,index_label=['bond_id','date'])
