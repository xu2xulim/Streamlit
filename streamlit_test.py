import streamlit as st

import streamlit.components.v1 as components
from streamlit_timeline import timeline
from deta import Deta
import os
import requests
import json

from datetime import datetime
import pytz
from dateutil.parser import parse

with st.expander("Open"):
    with st.form("Form", clear_on_submit=True):
        date = st.date_input("Date:")
        time = st.time_input("Time:", datetime.time(8,0))

        submit = st.form_submit_button("Submit")

        if submit:
            st.write(datetime.combine(date,time))
            st.write(datetime.combine(date,time).astimezone(pytz.timezone('UTC')))
