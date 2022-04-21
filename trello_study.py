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

with st.expander("Open to enter order details"):
    data = {'key' : st.secrets['TRELLO_API_KEY'], 'token' : st.secrets['TRELLO_TOKEN']}
    url_values = urllib.parse.urlencode(data)
    url = "https://api.trello.com/1/boards/611dc770573a0335f5d9fa11/cards?{}".format(url_values)
    result = urllib.request.urlopen(url)
    details = [x['badges'] for x in json.loads(result.read().decode('utf-8'))]
    st.write(details)
