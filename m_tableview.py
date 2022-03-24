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
res = httpx.get('https://cs0kji.deta.dev/board')

data = res.json()

board_list = (",".join(data['name'].keys()))


option = st.sidebar.selectbox(
    'How would you like to be contacted?',
    #('Email', 'Home phone', 'Mobile phone')
    board_list
)

if option == 'Email' :
    st.write('You selected:', option)
else:
# Add a slider to the sidebar:
    add_slider = st.sidebar.slider(
        'Select a range of values',
        0.0, 100.0, (25.0, 75.0)
        S)
