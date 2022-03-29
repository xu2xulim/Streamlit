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
