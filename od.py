import sqlite3
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

def get_data_from_bdd(txt):
    conn = sqlite3.connect(txt)
    cur = conn.cursor()
    dfflows=pd.read_sql_query("SELECT * FROM TU_GEO_LPW_MATRIX", conn)
    conn.close()
    return dfflows

#url='/Users/ismailsaadi/FNRS_research/uMOB/BELGIUM/ss/sh_statbel_statistical_sectors_20190101.shp'
#maps2=gpd.read_file(url)

df=get_data_from_bdd('data/TU_GEO_LPW_SECTOR.sqlite')

df['CD_REFINS_RESIDENCE']=[k.split('_')[1][:5] for k in df.CD_SECTOR_RESIDENCE]
df['CD_SECTOR_RESIDENCE_0']=[k.split('_')[1] for k in df.CD_SECTOR_RESIDENCE]
df['CD_SECTOR_RESIDENCE_PR']=[k.split('_')[1][0] for k in df.CD_SECTOR_RESIDENCE]

test=[]
for k in df.CD_SECTOR_WORK:
    if k=='FOR':
        test.append('FOR')
    else:
        test.append(k.split('_')[1][:5])

df['CD_REFINS_WORK']=test

test=[]
for k in df.CD_SECTOR_WORK:
    if k=='FOR':
        test.append('FOR')
    else:
        test.append(k.split('_')[1])
        
df['CD_SECTOR_WORK_0']=test

test=[]
for k in df.CD_SECTOR_WORK:
    if k=='FOR':
        test.append('FOR')
    else:
        test.append(k.split('_')[1][0])
        
df['CD_SECTOR_WORK_PR']=test

df['OBS_VALUE_NUM']=[int(k.split(',')[0]) for k in df['OBS_VALUE']]
#df_cp=df[['CD_SECTOR_WORK_0','OBS_VALUE_NUM']].groupby(['CD_SECTOR_WORK_0']).sum()

plt.imshow(pd.crosstab(index=df.CD_REFINS_RESIDENCE,columns=df.CD_REFINS_WORK, values=df.OBS_VALUE_NUM, aggfunc='sum').values, origin='lower', norm=LogNorm(vmin=0.01), cmap='OrRd')

plt.show()
