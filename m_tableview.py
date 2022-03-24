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
payload = {"board_id" : "", "list_id" : "", "card_id" : ""}
res = httpx.post('https://cs0kji.deta.dev/board',json=payload)
ll = []
["'{}'".format(x['name']) for x in res.json()['result']]


board_csv = "({})".format(", ".join(["'{}'".format(x['name']) for x in res.json()['result']]))
st.write(board_csv)
option = st.sidebar.selectbox(
    'How would you like to be contacted?',
    #('Email', 'Home phone', 'Mobile phone')
    board_csv)

"""
if option == 'Email' :
    st.write('You selected:', option)
else:
# Add a slider to the sidebar:
    option = st.sidebar.selectbox(
        'How would you like to be contacted?',
        #('Email', 'Home phone', 'Mobile phone')
        board_list)"""
