import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime
from deta import Deta
import json
import requests

import urllib.request
import urllib.parse
from trello import TrelloClient, List

def trello_client(key, tkn):
    client = TrelloClient(
        api_key = key,
        token = tkn,
        )
    mbr_id = client.fetch_json('members/me')['id']
    return (client, mbr_id)
#order = Deta(st.secrets["DETA_PROJECT_ID"]).Base("trello_orders")
st.header("Trello Study")

with st.expander("Open to test"):
    #data = {'key' : st.secrets['TRELLO_API_KEY'], 'token' : st.secrets['TRELLO_TOKEN']}
    #url_values = urllib.parse.urlencode(data)
    #url = "https://api.trello.com/1/cards/622aea41f4c5bd708e45fdd3?{}".format(url_values)
    #result = urllib.request.urlopen(url)
    (client, me) = trello_client(st.secrets['TRELLO_API_KEY'], st.secrets['TRELLO_TOKEN'])
    #card=client.get_card(json.loads(result.read().decode('utf-8'))['id'])
    card = client.get_card("622aea41f4c5bd708e45fdd3")
    st.header(card.name)
    st.subheader(card.desc)
    items = st.dataframe(card.checklists[0].items)
    items_sel = items[["state", "name", "due", "idMember"]]
    st.dataframe(items_sel)
