import streamlit as st

#import streamlit.components.v1 as components
from streamlit_timeline import timeline
from deta import Deta
import os
import requests
import json

#components.html(html, height=150)
#st.write("Something above")

db = Deta(os.environ.get('DETA_PROJECT_ID')).Base("item_alert")
res = db.fetch()
events = []
for itm in res.items:
    dd = {}
    due = itm['item_due']
    dd["start_date"] = {"month" : due[5:7], "day" : due[8:10], "year" :due[0:4]}
    dd["text"] = {"headline" : itm['item_state'], "text" : itm['item_name']}
    events.append(dd)

#event_dict = {}
#event_dict['events'] = events
#json_obj = json.dumps(event_dict)
#timeline(json_obj)

res = requests.post("https://70297.wayscript.io/timeline")

card_json = res.json()
for event in events:
    card_json['events'].append(event)

timeline(card_json)
