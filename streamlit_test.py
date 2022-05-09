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
    with st.form("Form", clear_on_submit=False):
        date = st.date_input("Date:")
        time = st.time_input("Time:")

        submit = st.form_submit_button("Submit")

        if submit:
            naive_datetime = datetime.combine(date,time)
            timezone = pytz.timezone('Asia/Singapore')
            aware_datetime = timezone.localize(naive_datetime)
            st.write(naive_datetime)
            st.write(aware_datetime)
