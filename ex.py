import streamlit as st 

pg = st.navigation([st.Page("player_registration.py", title="Registration"),st.Page("main.py", title="Create your account")], position="sidebar")
pg.run()