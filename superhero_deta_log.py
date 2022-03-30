import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime
from deta import Deta
import json
import requests

def unique(list1):
    x = np.array(list1)
    return np.unique(x)

log = alert = Deta("c0vidk60_8unssenvnHkuZmQfqhZ4jW49o5hRMvwG").Base('superhero_log')

res = log.fetch(query=None, limit=None, last=None)

dd = {}
for row in unique([x['mbr_id'] for x in res.items]) :
    if row not in dd.keys():
        dd[row] = {}
    for y in unique([x['datetime'][0:10] for x in res.items]):
        dd[row][y] = 0
st.write(dd)
for z in res.items :
    dd[z['mbr_id']][z['datetime'][0:10]] = dd[z['mbr_id']][z['datetime'][0:10]] + 1
dx = pd.DataFrame.from_dict(dd)(index=[x['datetime'][0:10] for x in res.items]])
st.dataframe(dx)
st.bar_chart(dx.astype(str))



df = pd.DataFrame.from_dict(res.items)
df['date']=df.datetime.str.slice(0, 10)
"""df1 = df.groupby(['endpoint', 'mbr_id', 'date']).count().fillna(0)
df2 = df1[['endpoint', 'mbr_id', 'date', 'key']]
st.dataframe(df2)
"""
df1 = df.groupby(['endpoint', 'mbr_id', 'date']).count()
#grouped_multiple.columns = ['endpoint', 'mbr_id', 'date', 'count']
df1 = df1.reset_index()
df2 = df1[['endpoint', 'mbr_id', 'date', 'key']]
#st.dataframe(df2)

st.bar_chart(df2[['date', 'key']].set_index('date'))

st.bar_chart(df2[['mbr_id', 'key']].set_index('mbr_id'))

st.bar_chart(df2[['endpoint', 'key']].set_index('endpoint'))

st.dataframe(df2)

columns = ['date']

for ix in range(0, len(df2.index)) :
    if df2.iloc[ix]['mbr_id'] not in columns:
        columns.append(df2.iloc[ix]['mbr_id'])

df3 = pd.DataFrame(columns=columns)

for ix in range(0, len(df2.index)) :
    dd = {}
    if df2.iloc[ix]['date'] in df3['date'].values:
        pass
    else:
        dd = {'date': df2.iloc[ix]['date']}
        df3 = df3.append(dd, ignore_index = True)

    for iz in range(0, len(df3.index)):
        if df2.iloc[ix]['date'] == df3.iloc[iz]['date']:
            df3[df2.iloc[ix]['mbr_id']].iloc[iz] = df2.iloc[ix]['key']
            break

df3 = df3.set_index('date')
chart_data = df3.fillna(0).astype(str).sort_values(by=['date'])
st.dataframe(chart_data)
st.bar_chart(chart_data)

##
