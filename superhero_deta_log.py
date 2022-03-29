import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime
from deta import Deta
import json
import requests

log = alert = Deta("c0vidk60_8unssenvnHkuZmQfqhZ4jW49o5hRMvwG").Base('superhero_log')

res = log.fetch(query=None, limit=None, last=None)

df = pd.DataFrame.from_dict(res.items)
df['date']=df1.datatine.str.slice(0, 10)
endpoint_mbr = df.groupby(['endpoint', 'mbr_id', 'date']).count().fillna(0)
st.dataframe(endpoint_mbr)
