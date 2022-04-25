import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

from datetime import datetime
from deta import Deta
import json
import requests

import urllib.request
import urllib.parse
from trello import TrelloClient, List

query_params = st.experimental_get_query_params()

@st.cache(suppress_st_warning=True)
def trello_client(key, tkn):
    client = TrelloClient(
        api_key = key,
        token = tkn,
        )
    mbr_id = client.fetch_json('members/me')['id']
    return (client, mbr_id)
#order = Deta(st.secrets["DETA_PROJECT_ID"]).Base("trello_orders")
def dl (url, key, tkn) :

    request = urllib.request.Request(url)
    request.add_header('Authorization', '''OAuth oauth_consumer_key="{}", oauth_token="{}"'''.format(key, tkn))
    webUrl  = urllib.request.urlopen(request)

    data = webUrl.read()
    return data



#st.header("Trello Study")
(client, me) = trello_client(st.secrets['TRELLO_API_KEY'], st.secrets['TRELLO_TOKEN'])
card = client.get_card(query_params['card_id'][0])
card_json = card._json_obj
#st.write(card_json)
cover = dl(card_json['cover']['scaled'][0]['url'], st.secrets['TRELLO_API_KEY'], st.secrets['TRELLO_TOKEN'])
st.image(cover)
st.header(card.name)

with st.expander("Open to see card labels"):
    #data = {'key' : st.secrets['TRELLO_API_KEY'], 'token' : st.secrets['TRELLO_TOKEN']}
    #url_values = urllib.parse.urlencode(data)
    #url = "https://api.trello.com/1/cards/622aea41f4c5bd708e45fdd3?{}".format(url_values)
    #result = urllib.request.urlopen(url)

    #card=client.get_card(json.loads(result.read().decode('utf-8'))['id'])
    lbl_color = '''<p style="color:{}">{}</p>'''
    card_labels = ""
    for lbl in card_json['labels']:
        if lbl['name'] == "":
            card_labels = card_labels + lbl_color.format(lbl['color'], lbl['color']) + " "
        else:
            card_labels = card_labels + lbl_color.format(lbl['color'], lbl['name']) + " "
    components.html(card_labels)

with st.expander("Open to see card start and due status"):
    #st. write(card_json)
    dates = {}
    dates['Start'] = card_json['start']
    dates['Due'] = card_json['due']
    dates['Completed?'] = card_json['dueComplete']

    st.json(dates)


with st.expander("Open to read card description"):
    st.markdown(card_json['desc'], unsafe_allow_html=False)

with st.expander("Open to inspect custom fields on card"):
    data = [{'name' : cf.name , 'value' : cf.value} for cf in card.custom_fields]
    #data = [{'name' : cf.name, 'value' : cf._value, 'type' : cf.field_type} for cf in card.custom_fields]
    st.json(data)

with st.expander("Open to see status of checklists on card"):
    for cl in card.checklists :
        st.write(cl.name)
        data = [{'state' : itm['state'], 'name' : itm['name'], 'due' : itm['due'], 'member' : itm['idMember']} for itm in cl.items]
        items = pd.DataFrame(data)
        items["state"].replace({"complete": "✅", "incomplete": "❌"}, inplace=True)
        st.dataframe(items)

with st.expander("Open to see images of attachments"):
