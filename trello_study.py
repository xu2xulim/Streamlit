import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime
from deta import Deta
import json
import requests

import urllib.request
import urllib.parse

#order = Deta(st.secrets["DETA_PROJECT_ID"]).Base("trello_orders")
st.header("Trello Study")

if st.session_state['focus'] == 1:
    with st.expander("Open to enter order details"):
        data = {'key' : st.secret('TRELO_API_KEY'), 'token' : st.secret('TRELO_TOKEN')}
        url_values = urllib.parse.urlencode(data)
        url = "https://trello.com/b/SsRevba7/project-archives.json?{}".format(url_values)
        result = urllib.request.urlopen(url)
        json_obj = json.loads(result.read().decode('utf-8'))
        st.json(json_obj)
