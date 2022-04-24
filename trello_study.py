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

with st.expander("Open to test"):
    data = {'key' : st.secrets['TRELLO_API_KEY'], 'token' : st.secrets['TRELLO_TOKEN']
    url_values = urllib.parse.urlencode(data)
    url = "https://api.trello.com/1/cards/622aea41f4c5bd708e45fdd3?{}".format(url_values)
    result = urllib.request.urlopen(url)

    st.write(result)
