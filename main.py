import streamlit as st
import pandas as pd
import pyodbc
import urllib
from sqlalchemy import create_engine



# st.set_page_config(page_title="Game Management", page_icon="🎮")
# Driver={ODBC Driver 18 for SQL Server};Server=tcp:bhushankoahadkar.database.windows.net,1433;Database=Game;Uid=bhushankohadkar;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;
# Function to connect to SQL Server
# def get_connection():
    # return pyodbc.connect(
    #     "DRIVER={ODBC Driver 17 for SQL Server};"
    #     "SERVER=DESKTOP-UK7PLJM\\SQLEXPRESS;"
    #     "DATABASE=Game;"
    #     "Trusted_Connection=yes;"
    # )

    #  return pyodbc.connect(
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

# Function to fetch registered players from Registration table
def get_registered_players():
    conn = get_connection()
    query = "SELECT ID, PlayerName FROM Registration ORDER BY PlayerName"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to insert game results
def insert_game_result(match_number, player_id, kills, deaths, score, game_winner, total_score, tokens):
    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO MatchResults (MatchNumber, PlayerID, Kills, Deaths, Score, GameWinner, TotalScore, Tokens)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(query, (match_number, player_id, kills, deaths, score, game_winner, total_score, tokens))
    conn.commit()
    conn.close()

# Function to fetch match results
def get_game_results():
    conn = get_connection()
    query = """SELECT m.MatchNumber, r.PlayerName, m.Kills, m.Deaths, m.Score, m.GameWinner, m.TotalScore, m.Tokens
               FROM MatchResults m
               JOIN Registration r ON m.PlayerID = r.ID
               ORDER BY m.MatchNumber DESC"""
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Streamlit UI

# st.sidebar.title("🔹 Navigation")
# st.sidebar.page_link("pages/player_registration.py", label="Register Player")

# pages = {
#     "Home Page": [
#         st.Page("main.py", title="Create your account"),
#         st.Page("pages/player_registration.py", title="Registration"),
#     ]
# }

# ✅ Create Navigation in Sidebar
# pg = st.navigation([st.Page("pages/player_registration.py", title="Registration"),st.Page("main.py", title="Create your account")], position="sidebar")
# pg.run()
# ✅ Run the Navigation System
# pg.run()
# Register = st.Page("pages/player_registration.py", title ="Register Player")
# pg = st.navigation([Register],position="sidebar")
# pg.run()
# Home=st.page_link("main.py", label="Home", icon="🏠")

# pg = st.navigation(
#     [ Home],
#     position="hidden",
# )
# pg.run()


st.title("🎮 Game Results Management")

# Load registered players for selection
players_df = get_registered_players()
if players_df.empty:
    st.warning("⚠ No players found. Please register players first!")
    st.stop()

# Dropdown: Select Player
player_options = {row["PlayerName"]: row["ID"] for _, row in players_df.iterrows()}  # Dictionary {PlayerName: PlayerID}

# Form to insert game data
with st.form("game_result_form"):
    match_number = st.number_input("Match Number", min_value=1, step=1)
    selected_player_name = st.selectbox("Select Player", list(player_options.keys()))  # Display Player Names
    player_id = player_options[selected_player_name]  # Fetch corresponding PlayerID
    kills = st.number_input("Kills", min_value=0)
    deaths = st.number_input("Deaths", min_value=0)
    score = kills - deaths  # Auto-calculate score
    game_winner = st.text_input("Game Winner")
    total_score = st.number_input("Total Score", min_value=0)
    tokens = st.number_input("Tokens", min_value=0)

    submitted = st.form_submit_button("Add Game Result")
    if submitted:
        insert_game_result(match_number, player_id, kills, deaths, score, game_winner, total_score, tokens)
        st.success(f"✅ Game result for {selected_player_name} (Match {match_number}) added!")

# Display game results
st.subheader("📊 Game Results Table")
game_results_df = get_game_results()
st.dataframe(game_results_df)
