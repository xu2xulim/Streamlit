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


columns = ['date', 'key']

for ix in range(0, len(df2.index)) :
    if df2.iloc[ix]['mbr_id'] not in columns:
        columns.append(df2.iloc[ix]['mbr_id'])

st.write(columns)
df3 = pd.DataFrame(columns=columns)
df3.set_index('date')


for ix in range(0, len(df2.index)) :
    if df2.iloc[ix]['date'] not in df3['date'].keys() :
        df3[df2.iloc[ix]['date']] = {}
    else:
        df3[df2.iloc[ix]['date']][df2.iloc[ix]['mbr_id']] = df2.iloc[ix]['key']

st.dataframe(df3)
st.bar_chart(df3)
# Vertical stacked bar chart
st.bar_chart(chart_data)
##
