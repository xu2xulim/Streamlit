import streamlit as st
import pandas as pd
import numpy as np

from deta import Deta
import json

# 2) initialize with a project key
deta = Deta("c0vidk60_8unssenvnHkuZmQfqhZ4jW49o5hRMvwG")

# 3) create and use as many DBs as you want!
db = deta.Base("trello_movement")

res = db.fetch(query = None, limit=1000, last=None)

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = res.items
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')
#st.dataframe(data=data, width=None, height=None)
req_columns = [[col['listAfter'], col['listBefore']] for col in res.items]

df = pd.DataFrame (req_columns, columns = ['After', 'Before'])
#st.write(df)
mov_in = df.loc[df['After'] == 'Up Next']
mov_out = df.loc[df['Before'] == 'Up Next']
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="When", value='Now')
col2.metric(label="Move In", value=mov_in[mov_in.columns[0]].count())
col3.metric(label="Move Out", value=mov_out[mov_out.columns[0]].count())
col4.metric(label="On List", value=(mov_in[mov_in.columns[0]].count()-mov_out[mov_out.columns[0]].count()))

summary = deta.Base("trello_movement_summary")
res = summary.fetch(query = None, limit=1000, last=None)
output = pd.DataFrame()
output.columns = ['Date', 'Move In', 'Move Out', 'On List']
for col in res.items:
    col.update(abs(int(col['mov_in'])-int(col['mov_out']))
    output = output.append(col, ignore_index=True)

st.write(output)
