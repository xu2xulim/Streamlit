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

df3 = pd.DataFrame()
df3.columns('date', 'mbr_r', 'key')
for ix in range(0, len(df2.index)) :

    df3[df2.iloc[ix]['date']][df2.iloc[ix]['mbr_id']] = df2.iloc[ix]['key'].item

st.dataframe(df3)
# Vertical stacked bar chart
st.bar_chart(chart_data)
