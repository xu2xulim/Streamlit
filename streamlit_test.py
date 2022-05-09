import streamlit as st

import streamlit.components.v1 as components
from streamlit_timeline import timeline
from deta import Deta
import os
import requests
import json

with st.expander("Open"):
    with st.form("", clear_on_submit=True):
        date = st.date_input("Date:")
        time = st.time_input("Time:")

        submit = st.form_submit_button("Submit")

        if submit:
            st.write()
