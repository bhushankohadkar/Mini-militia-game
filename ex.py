import streamlit as st 

pg = st.navigation([st.Page("pages/player_registration.py", title="Registration"),st.Page("pages/main.py", title="Create your account")], position="sidebar")
pg.run()