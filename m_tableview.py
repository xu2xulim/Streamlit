import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime
from deta import Deta
import json
import httpx

# 2) initialize with a project key
#deta = Deta(st.secrets["tableview"])

# 3) create and use as many DBs as you want!
#db = deta.Base(st.secrets["MOVEMENT"])
#today = datetime.today().strftime('%Y-%m-%d')
#res = db.fetch(query = {'date' : today}, limit=1000, last=None)

# Create a text element and let the reader know the data is loading.
#data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
#data = res.items
# Notify the reader that the data was successfully loaded.

#st.dataframe(data=data, width=None, height=None)
board_id = ""
list_id = ""
card_id = ""
selected_board = ""
payload = {"board_id" : board_id, "list_id" : list_id, "card_id" : card_id}
res = httpx.post('https://cs0kji.deta.dev/board',json=payload)
df = pd.DataFrame(res.json()['result'])
selected_board = st.sidebar.selectbox(
    'Select a board', options=df['name'])

if selected_board != "":
    bd = next(x for x in res.json()['result'] if x['name'] == selected_board)
    payload = {"board_id" : bd['id'], "list_id" : list_id, "card_id" : card_id}
    res = httpx.post('https://cs0kji.deta.dev/list',json=payload)
    df = pd.DataFrame(res.json()['result'])
    selected_col = ""
    selected_col = st.sidebar.selectbox(
        'Select a list', options=df['name'])

    if selected_col !="" :
        item = next(x for x in res.json()['result'] if x['name'] == selected_col)
        payload = {"board_id" : bd['id'], "list_id" : item['id'], "card_id" : ""}
        res = httpx.post('https://cs0kji.deta.dev/cards',json=payload)
        data = res.json()['result']
        #st.write(data)

        rows = []

        # appending rows
        for item in data:
            item_row = item['customfield']
            crd = item['card']

            for row in item_row:
                row['card']= crd
                rows.append(row)

                # using data frame
        df_x = pd.DataFrame(rows)
        st.dataframe(df_x)#df = pd.DataFrame(data['card'].values())
