import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime
from deta import Deta
import json
import requests

def unique(list1):
    x = np.array(list1)
    return np.unique(x)

log = alert = Deta("c0vidk60_8unssenvnHkuZmQfqhZ4jW49o5hRMvwG").Base('superhero_log')

res = log.fetch(query=None, limit=None, last=None)

dd = {}
##Start
for row in unique([x['mbr_id'] for x in res.items]) :
    if row not in dd.keys():
        dd[row] = {}
    for y in unique([x['datetime'][0:10] for x in res.items]):
        dd[row][y] = 0

for z in res.items :
    dd[z['mbr_id']][z['datetime'][0:10]] = dd[z['mbr_id']][z['datetime'][0:10]] + 1
d_mbr = pd.DataFrame.from_dict(dd)
st.header('Daily usage by member')
st.dataframe(d_mbr)
st.bar_chart(d_mbr)

##Start
dd = {}
for row in unique([x['endpoint'] for x in res.items]) :
    if row not in dd.keys():
        dd[row] = {}
    for y in unique([x['datetime'][0:10] for x in res.items]):
        dd[row][y] = 0

for z in res.items :
    dd[z['endpoint']][z['datetime'][0:10]] = dd[z['endpoint']][z['datetime'][0:10]] + 1
d_endpoint = pd.DataFrame.from_dict(dd)
st.header('Daily usage by endpoint')
st.dataframe(d_endpoint)
st.bar_chart(d_endpoint)
