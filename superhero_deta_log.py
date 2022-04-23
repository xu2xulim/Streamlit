import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import numpy as np
import os
from datetime import datetime
from deta import Deta
import json
import requests

def unique(list1):
    x = np.array(list1)
    return np.unique(x)

log = alert = Deta(os.environ.get('DETA_PROJECT_ID')).Base('superhero_log')
Users=Deta(os.environ.get('DETA_PROJECT_ID')).Base(os.environ.get('MILYNNUS_ST_USERS_BASE'))

res = Users.fetch(query=None, limit=100, last=None)
names = []
usernames = []
hashed_passwords = []
for x in res.items :
    names.append(x['name'])
    usernames.append(x['username'])
    hashed_passwords[x['hash_password']]

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    'milynnus_stauth', os.environ.get('MILYNNUS_ST_USERS_SIGNATURE'), cookie_expiry_days=30)

name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state['authentication_status']:
    authenticator.logout('Logout', 'main')
    st.write('Welcome *%s*' % (st.session_state['name']))
    st.title('Some content')
elif st.session_state['authentication_status'] == False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] == None:
    st.warning('Please enter your username and password')


res = log.fetch(query=None, limit=None, last=None)
unique_mbr = unique([x['mbr_id'] for x in res.items])
unique_endpoints = unique([x['endpoint'] for x in res.items])
unique_dates = unique([x['datetime'][0:10] for x in res.items])
states = st.session_state

if 'saved_mbr_num' not in st.session_state or  'saved_end_num' not in st.session_state or 'saved_req_num' not in st.session_state:
    st.session_state['saved_mbr_num'] = len(unique_mbr)
    st.session_state['saved_end_num'] = len(unique_endpoints)
    st.session_state['saved_req_num'] = len(res.items)

st.title('7 Day Superhero Dashboard')

st.header('Metrics')
col1, col2, col3, col4= st.columns(4)
col1.metric(label="Days", value=len(unique_dates))
col2.metric(label="Active Members", value=len(unique_mbr), delta = (len(unique_mbr)-st.session_state['saved_mbr_num']))
col3.metric(label="Active Endpoints", value=len(unique_endpoints), delta = (len(unique_endpoints)-st.session_state['saved_end_num']))
col4.metric(label="All Requests", value=len(res.items), delta = (len(res.items)-st.session_state['saved_req_num']) )

st.session_state['saved_mbr_num'] = len(unique_mbr)
st.session_state['saved_end_num'] = len(unique_endpoints)
st.session_state['saved_req_num'] = len(res.items)
dd = {}
##Start
for row in unique_mbr :
    if row not in dd.keys():
        dd[row] = {}
    for y in unique_dates:
        dd[row][y] = 0

for z in res.items :
    dd[z['mbr_id']][z['datetime'][0:10]] = dd[z['mbr_id']][z['datetime'][0:10]] + 1
d_mbr = pd.DataFrame.from_dict(dd)

st.header('Daily usage by member')
st.dataframe(d_mbr)
st.bar_chart(d_mbr)

##Start
dd = {}
for row in unique_endpoints :
    if row not in dd.keys():
        dd[row] = {}
    for y in unique_dates:
        dd[row][y] = 0

for z in res.items :
    dd[z['endpoint']][z['datetime'][0:10]] = dd[z['endpoint']][z['datetime'][0:10]] + 1
d_endpoint = pd.DataFrame.from_dict(dd)
st.header('Daily usage by endpoint')
st.dataframe(d_endpoint)
st.bar_chart(d_endpoint)

result = d_mbr.to_json(orient="split")
parsed = json.loads(result)

res = requests.post("https://68359.wayscript.io/st_members", json=parsed)
