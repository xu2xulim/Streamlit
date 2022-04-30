import streamlit as st

import streamlit.components.v1 as components
import streamlit_timeline as timeline
from deta import Deta
import os
st.write("Something below")
"""components.html('''<blockquote class="trello-card-compact">
  <a href="https://trello.com/c/AKtsBUPw/79-setup-your-smtp-on-contalist-and-test">Trello Card</a>
</blockquote>
<script src="https://p.trellocdn.com/embed.min.js"></script>''')"""
html = '''<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <style></style>
        <script></script>
    </head>
    <body>
        <img src="https://cdn.wayscript.com/static/img/logos/logo.png">
        <!-- <div>Hello World</div> -->
        <blockquote class="trello-card-compact">
          <a href="https://trello.com/c/AKtsBUPw/79-setup-your-smtp-on-contalist-and-test">Trello Card</a>
        </blockquote>
        <script src="https://p.trellocdn.com/embed.min.js"></script>
    </body>
</html>'''

components.html(html, height=150)
st.write("Something above")

db = Deta(os.environ.get('DETA_PROJECT_ID').Base("item_alert")
res = db.fetch()
json_obj = st.json(res.items)
timeline(json_obj)
