from deta import Deta
import json

# 2) initialize with a project key
deta = Deta("c0vidk60_8unssenvnHkuZmQfqhZ4jW49o5hRMvwG")

# 3) create and use as many DBs as you want!
db = deta.Base("trello_base")

res = db.fetch(query = None, limit=1000, last=None)

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = res.items
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

st.subheader('Raw data')
st.write(data)
