import streamlit as st 
import pyodbc
from datetime import datetime

# Database connection
def get_connection():
    # return pyodbc.connect(
    #     "DRIVER={ODBC Driver 17 for SQL Server};"
    #     "SERVER=DESKTOP-UK7PLJM\\SQLEXPRESS;"
    #     "DATABASE=Game;"
    #     "Trusted_Connection=yes;"
    # )

    # return pyodbc.connect(
    #     "DRIVER={ODBC Driver 18 for SQL Server};"
    #     "SERVER=tcp:bhushankoahadkar.database.windows.net,1433;"
    #     "DATABASE=Game;"
    #     "UID=bhushankohadkar;"
    #     "PWD=Bhushank@11;"
    #     "Encrypt=yes;"
    #     "TrustServerCertificate=no;"
    #     "Connection Timeout=30;"
    # )
    connection_string = urllib.parse.quote_plus(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=tcp:bhushankoahadkar.database.windows.net,1433;"
        "DATABASE=Game;"
        "UID=bhushankohadkar;"
        "PWD=your_password_here;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")
    return engine.connect()

# Function to insert a new player
def insert_player(PlayerName, DateOfJoin):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Convert DateOfJoin to string (YYYY-MM-DD) for SQL Server
    DateOfJoin_str = DateOfJoin.strftime('%Y-%m-%d')
    
    query = "INSERT INTO Registration (PlayerName, DateOfJoin) VALUES (?, ?)"
    cursor.execute(query, (PlayerName, DateOfJoin_str))
    
    conn.commit()
    conn.close()

# Streamlit UI
st.set_page_config(page_title="Register Player", page_icon="📝")

st.title("📝 Register New Player")

# Input Fields
PlayerName = st.text_input("Enter Player Name")

# Manual Date Picker (Calendar)
DateOfJoin = st.date_input("Select Registration Date")  # User must choose a date

if st.button("Register Player"):
    if PlayerName and DateOfJoin:
        insert_player(PlayerName, DateOfJoin)
        st.success(f"✅ Player '{PlayerName}' registered successfully on {DateOfJoin}!")
    else:
        st.warning("⚠️ Please enter a player name and select a registration date.")
