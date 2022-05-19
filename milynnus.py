import streamlit as st
#import pandas as pd
#import numpy as np
#import streamlit.components.v1 as components
import streamlit_authenticator as stauth
from streamlit_folium import folium_static
import folium

import os
from datetime import datetime
from deta import Deta
import json
#import requests

#import urllib.request
#import urllib.parse
#from trello import TrelloClient, List
#from dateutil.parser import parse
from datetime import datetime
import pytz
tz = pytz.timezone('Asia/Singapore')

@st.cache(suppress_st_warning=True)
def auth_init():

    res = Users.fetch(query=None, limit=100, last=None)
    names = []
    usernames = []
    hashed_passwords = []
    for x in res.items :
        names.append(x['name'])
        usernames.append(x['username'])
        hashed_passwords.append(x['hash_password'])

    return names, usernames, hashed_passwords

Users=Deta(os.environ.get('DETA_PROJECT_ID')).Base(os.environ.get('MILYNNUS_ST_USERS_BASE'))

with st.sidebar:
    st.title("Trello Share A Card")
    st.info("This application is secured by Streamlit-Authenticator.")
    names, usernames, hashed_passwords = auth_init()
    authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
        'milynnus_stauth', os.environ.get('MILYNNUS_ST_USERS_SIGNATURE'), cookie_expiry_days=30)

    name, authentication_status, username = authenticator.login('Login', 'sidebar')

    if st.session_state['authentication_status']:
        authenticator.logout('Logout', 'main')
        st.write('Welcome *%s*' % (st.session_state['name']))

        res = Users.fetch(query={"name" : name, "username" : username}, limit=None, last=None)
        if len(res.items) == 1:
            user = Users.get(res.items[0]["key"])
            card_dict = {}
            if "shared_cards" in user.keys():
                for url in user["shared_cards"] :
                    card_json = get_card_json(url)
                    card_dict[card_json['name']] = card_json['id']

        option = st.selectbox(
            'Select the card you like to see',
            options=list(card_dict.keys()))

        st.write('You selected:', option)
        st.session_state['card_id'] = card_dict[option]
    elif st.session_state['authentication_status'] == False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] == None:
        st.warning('Please enter your username and password')

    if not st.session_state['authentication_status']:
        with st.expander("Register"):
            st.warning("This form is for user self registration. The registration data is kept in a Deta Base.")
            with st.form("Fill in your name, your preferred username and password", clear_on_submit=True):
                name = st.text_input("Name")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                username_unique = Users.fetch(query={"username" : username})
                submit = st.form_submit_button("Submit")
                if username_unique.count == 0:
                    pass
                else:
                    st.write("The username : {} has been used, please use another preferred username.".format(username))
                    st.stop()

                if submit:
                    Users.put({'name' : name, 'username' : username, 'hash_password' : stauth.Hasher([password]).generate()[0]})

        with st.expander("Admin setup"):
            st.warning("This form is used by the administrator to attach card urls to a username. An admin secret is required for the update.")
            with st.form("Enter the card url to be shared with the user", clear_on_submit=True):
                username = st.text_input("Username")
                url = st.text_input("Card URL")
                admin_secret = st.text_input("Admin Secret", type="password")

                submit = st.form_submit_button("Submit")

                if submit and admin_secret == os.environ.get('MILYNNUS_ST_USERS_SIGNATURE'):
                    users = Users.fetch(query={"username" : username}, limit=None, last=None)
                    if len(users.items) != 1 :
                        st.write("User is not found")
                    else:
                        st.write(users.items[0]["key"])
                        user = Users.get(users.items[0]["key"])
                        try :
                            shared_cards = user['shared_cards']
                        except:
                            shared_cards = []
                        if url in shared_cards :
                            st.write("Card with url {} is already shared with {}".format(url, username))
                        else:
                            shared_cards.append(url)
                            Users.update({"shared_cards" : shared_cards }, user["key"])
                            st.write("Card with url {} is shared with {}".format(url, username))

if not st.session_state['authentication_status']  :
    st.stop()
