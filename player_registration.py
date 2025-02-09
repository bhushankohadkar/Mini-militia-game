import streamlit as st 
import pyodbc
from datetime import datetime
import urllib
from sqlalchemy import create_engine

# Database connection
# def get_connection():
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
    # connection_string = urllib.parse.quote_plus(
    #     "DRIVER={ODBC Driver 18 for SQL Server};"
    #     "SERVER=tcp:bhushankoahadkar.database.windows.net,1433;"
    #     "DATABASE=Game;"
    #     "UID=bhushankohadkar;"
    #     "PWD=your_password_here;"
    #     "Encrypt=yes;"
    #     "TrustServerCertificate=no;"
    #     "Connection Timeout=30;"
    # )
    
    # engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")
    # return engine.connect()

def get_connection():
    server = "tcp:bhushankoahadkar.database.windows.net,1433"  # Replace with your Azure SQL Server
    database = "Game"
    username = "bhushankohadkar"
    password = "Bhushank@11"
    
    driver = "ODBC Driver 18 for SQL Server"  # Ensure this is installed

    connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

    try:
        # Using pyodbc
        conn = pyodbc.connect(connection_string)
        print("✅ Successfully connected using pyodbc")
        return conn

    except Exception as e:
        print(f"❌ Error connecting using pyodbc: {e}")
    
    try:
        # Using SQLAlchemy with pyodbc
        params = urllib.parse.quote_plus(connection_string)
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
        conn = engine.connect()
        print("✅ Successfully connected using SQLAlchemy")
        return conn

    except Exception as e:
        print(f"❌ Error connecting using SQLAlchemy: {e}")

    return None

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
