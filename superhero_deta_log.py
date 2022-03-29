import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime
from deta import Deta
import json
import requests

log = alert = Deta("c0vidk60_8unssenvnHkuZmQfqhZ4jW49o5hRMvwG").Base('superhero_log')

res = log.fetch(query=None, limit=None, last=None)

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

chart_data = pd.DataFrame(
    np.random.rand(9, 4),
    index=["air","coffee","orange","whitebread","potato","wine","beer","wheatbread","carrot"],
)
st.dataframe(chart_data)
st.dataframe(df2)

columns = ['date']

for ix in range(0, len(df2.index)) :
    if df2.iloc[ix]['mbr_id'] not in columns:
        columns.append(df2.iloc[ix]['mbr_id'])

df3 = pd.DataFrame(columns=columns)
df3.set_index('date')


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





chart_data3 = df3.fillna(0).astype(str)
st.bar_chart(chart_data3)
# Vertical stacked bar chart
st.bar_chart(chart_data)
##
