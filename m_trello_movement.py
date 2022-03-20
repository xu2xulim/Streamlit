import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime
from deta import Deta
import json

# 2) initialize with a project key
deta = Deta(st.secrets["DETA_PROJECT"])

# 3) create and use as many DBs as you want!
db = deta.Base(st.secrets["MOVEMENT"])
today = datetime.today().strftime('%Y-%m-%d')
res = db.fetch(query = {'date' : today}, limit=1000, last=None)

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = res.items
# Notify the reader that the data was successfully loaded.

#st.dataframe(data=data, width=None, height=None)
req_columns = [[col['idList'], col['listAfter'], col['listBefore']] for col in res.items]
df = pd.DataFrame (req_columns, columns = ['idList', 'After', 'Before'])
#st.write(df)
mov_in = df.loc[df['After'] == df['idList']]
mov_out = df.loc[df['Before'] == df['idList']]
data_load_state.text('Loading data...done!')
st.header('Movement Dashboard')
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="When", value='Now')
col2.metric(label="Move In", value=mov_in[mov_in.columns[0]].count())
col3.metric(label="Move Out", value=mov_out[mov_out.columns[0]].count())
col4.metric(label="On List", value=str(db.get(data[0]['idList'])['control']))

summary = deta.Base(st.secrets["SUMMARY"])
#st.write(summary)
res = summary.fetch(query = None, limit=1000, last=None)
#st.write(res.items)
output = pd.DataFrame()
for col in res.items:
    output = output.append(col, ignore_index=True)

output.columns = ['Date', 'Move In', 'Move Out', 'On List']
st.header('Daily summary')
st.table(output)
