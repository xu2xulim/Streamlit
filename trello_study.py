import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime
from deta import Deta
import json
import requests

import urllib.request
import urllib.parse


def explore(df):
  # DATA
  st.write('Data:')
  st.write(df)
  # SUMMARY
  df_types = pd.DataFrame(df.dtypes, columns=['Data Type'])
  numerical_cols = df_types[~df_types['Data Type'].isin(['object',
                   'bool'])].index.values
  df_types['Count'] = df.count()
  df_types['Unique Values'] = df.nunique()
  df_types['Min'] = df[numerical_cols].min()
  df_types['Max'] = df[numerical_cols].max()
  df_types['Average'] = df[numerical_cols].mean()
  df_types['Median'] = df[numerical_cols].median()
  df_types['St. Dev.'] = df[numerical_cols].std()
  st.write('Summary:')
  st.write(df_types)
def get_df(file):
  # get extension and read file
  extension = file.name.split('.')[1]
  if extension.upper() == 'CSV':
    df = pd.read_csv(file)
  elif extension.upper() == 'XLSX':
    df = pd.read_excel(file, engine='openpyxl')
  elif extension.upper() == 'PICKLE':
    df = pd.read_pickle(file)
  return df
  
#order = Deta(st.secrets["DETA_PROJECT_ID"]).Base("trello_orders")
st.header("Trello Study")

with st.expander("Open to enter order details"):
    data = {'key' : st.secrets['TRELLO_API_KEY'], 'token' : st.secrets['TRELLO_TOKEN']}
    url_values = urllib.parse.urlencode(data)
    url = "https://api.trello.com/1/boards/5fdd53039a97d380e792101e/cards?{}".format(url_values)
    result = urllib.request.urlopen(url)
    dd = {}
    for x in json.loads(result.read().decode('utf-8')) :
        if x['idList'] in dd.keys():
            pass
        else:
            dd[x['idList']] = 0
        dd[x['idList']] += 1

    st.write(dd)

    file = st.file_uploader("A .csv file representing your checklist with name, due date(optional), assigned(optional)", type=['csv'])

    if not file:
        st.write("Upload a .csv or .xlsx file to get started")
        return
    df = get_df(file)
    explore()
