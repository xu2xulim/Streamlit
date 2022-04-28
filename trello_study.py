import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import streamlit_authenticator as stauth

import os
from datetime import datetime
from deta import Deta
import json
import requests

import urllib.request
import urllib.parse
from trello import TrelloClient, List

#query_params = st.experimental_get_query_params()
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

@st.cache(suppress_st_warning=True)
def trello_client(key, tkn):
    client = TrelloClient(
        api_key = key,
        token = tkn,
        )
    mbr_id = client.fetch_json('members/me')['id']
    return (client, mbr_id)
#order = Deta(st.secrets["DETA_PROJECT_ID"]).Base("trello_orders")
@st.cache(suppress_st_warning=True)
def dl (url, key, tkn) :

    request = urllib.request.Request(url)
    request.add_header('Authorization', '''OAuth oauth_consumer_key="{}", oauth_token="{}"'''.format(key, tkn))
    webUrl  = urllib.request.urlopen(request)

    data = webUrl.read()
    return data

#@st.cache(suppress_st_warning=True)
def get_card_json (url):

    res = requests.post('https://cs0kji.deta.dev/url2json', json={"url" : url})
    if res.status_code == 200 :
        return res.json()
    else:
        return {}
    """data = {'key' : st.secrets['TRELLO_API_KEY'], 'token' : st.secrets['TRELLO_TOKEN']}
    url_values = urllib.parse.urlencode(data)
    url = "{}.json?{}".format(url, url_values)
    result = urllib.request.urlopen(url)
    card_json = json.loads(result.read().decode('utf-8'))
    return card_json"""


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

if 'card_id' in st.session_state:
    card_id = st.session_state['card_id']
#st.header("Trello Study")
"""(client, me) = trello_client(st.secrets['TRELLO_API_KEY'], st.secrets['TRELLO_TOKEN'])
card = client.get_card(card_id)
card_json = card._json_obj"""

res = requests.post('https://cs0kji.deta.dev/card_json', json={"card_id" : card_id})
if res.status_code == 200 :
    card_json=res.json()
else:
    st.stop()
#st.write(card_json)
if card_json['idAttachmentCover'] == None and card_json['manualCoverAttachment'] == True :
    request = urllib.request.Request(card_json['cover']['scaled'][-1]['url'])
    #request.add_header('Authorization', '''OAuth oauth_consumer_key="{}", oauth_token="{}"'''.format(key, tkn))
    webUrl  = urllib.request.urlopen(request)

    st.image(webUrl.read())
else:
    cover = dl(card_json['cover']['scaled'][-1]['url'], st.secrets['TRELLO_API_KEY'], st.secrets['TRELLO_TOKEN'])
    st.image(cover)

st.header(card_json['name'])

with st.expander("Open to see card labels"):

    lbl_color='''<p id="px", style="background-color:{};color:{};font-size:150%;border: 1px solid black;">{}</p>'''
    #lbl_color = '''<p style="color:{}">{}</p>'''
    card_labels = '''<head><style>#px{display:inline;}</style></head><body>'''
    for lbl in card_json['labels']:
        #color_patch =  "{:<15}".format(lbl['color'])
        if lbl['color'] != None :
            color_patch = lbl['color'].rjust(5, '*')

        if lbl['name'] == "":
            card_labels = card_labels + lbl_color.format(lbl['color'],lbl['color'], color_patch) + "   "
        else:
            if lbl['color'] == 'yellow' or lbl['color'] == None:
                card_labels = card_labels + lbl_color.format(lbl['color'], 'black', lbl['name']) + "   "
            else:
                card_labels = card_labels + lbl_color.format(lbl['color'], 'white', lbl['name']) + "   "

    card_labels=card_labels + "</body>"
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
    res = requests.post('https://cs0kji.deta.dev/card_customfields', json={"card_id" : card_id})
    if res.status_code == 200 :
        st.json(res.json())

with st.expander("Open to see status of checklists on card"):

    res = requests.post('https://cs0kji.deta.dev/card_checklistitems', json={"card_id" : card_id})
    if res.status_code == 200 :
        checklist_d = res.json()
        for cl in checklist_d.keys():
            st.write(cl)

        #data = [{'state' : itm['state'], 'name' : itm['name'], 'due' : itm['due'], 'member' : assigned_name } for itm in cl.items]
            items = pd.DataFrame(checklist_d[cl]).fillna("Not Available")
            items["state"].replace({"complete": "✅", "incomplete": "❌"}, inplace=True)
            st.dataframe(items)

with st.expander("Open to see images of attachments"):
    columns = st.columns(5)
    ix = 0
    res = requests.post('https://cs0kji.deta.dev/card_attachments', json={"card_id" : card_id})
    if res.status_code == 200 :
        for attach in res.json()['attachments']:
            ext = attach['name'].split(".")[-1]
            if (ext == 'jpg' or ext == 'png' or ext == 'jpeg') and attach['id'] != card_json['idAttachmentCover'] and ix <5:
                res = requests.post('https://cs0kji.deta.dev/get_attachment', json={"url" : attach['url']})
                #data = dl(attach['url'],st.secrets['TRELLO_API_KEY'], st.secrets['TRELLO_TOKEN'] )

                data = bytes(res.json()['bytes'], 'ascii')
                with columns[ix]:
                    columns[ix].image(data)
                ix += 1
