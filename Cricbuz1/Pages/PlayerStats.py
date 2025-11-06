import streamlit as st
import requests
import pandas as pd

# ✅ API URLs with dynamic ID placeholder
url_search = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"
url_player = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}"
url_batting = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/batting"
url_bowling = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/bowling" 

headers = {
	"x-rapidapi-key": "7e5b05e398msh119c4d3f390c978p17a289jsnf8083a4db932",
	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

st.set_page_config(page_title="Cricket Player Statistics", layout="wide")
st.title("🏏 Cricket Player Statistics")

def search_player(name):
    return requests.get(url_search, headers=headers, params={"plrN": name}).json()

def get_player_stats(player_id):
    return requests.get(url_player.format(player_id=player_id), headers=headers).json()

# Player search input
col1, col2 = st.columns([4, 1])
with col1:
    player_name = st.text_input("Enter player name:", placeholder="e.g., Virat Kohli")
with col2:
    search_btn = st.button("Search")

# Session state variables
if "players" not in st.session_state:
    st.session_state.players = {}
if "selected_player" not in st.session_state:
    st.session_state.selected_player = None



# ✅ Search triggered
if search_btn and player_name.strip():
    response = requests.get(url_search, headers=headers, params={"plrN": player_name})
    
    if response.status_code == 200:
        data = response.json()
        if "player" in data and len(data["player"]) > 0:
            st.session_state.players = {p["name"]: p["id"] for p in data["player"]}
        else:
            st.warning("No player found. Try a different name.")
    else:
        st.error("API Error while searching players.")

# ✅ If player list available
if st.session_state.players:
    selected_player = st.selectbox("Select a player:", list(st.session_state.players.keys()))
    st.session_state.selected_player = selected_player

# ✅ Fetch player details
if st.session_state.selected_player:
    player_id = st.session_state.players[st.session_state.selected_player]
    player_resp = requests.get(url_player.format(player_id=player_id), headers=headers)

    if player_resp.status_code == 200:
        player_data = player_resp.json()

        st.header(f"📌 {player_data.get('name', '')} - Player Profile")
        st.subheader(player_data.get("nickName", ""))

        Profile,Batting, Bowling = st.tabs(["Profile","Batting Stats", "Bowling Stats"])
        with Profile:
            st.header("📌 personal Information")

            #st.write("Country:", player_data.get("country", "N/A"))
            st.write("Role:", player_data.get("role", "N/A"))
            st.write("Batting Style:", player_data.get("bat", "N/A"))
            st.write("Bowling Style:", player_data.get("bowl", "N/A"))
            st.write("International Team:", player_data.get("country", "N/A"))

# BATTING details

        with Batting:
            st.subheader("📈 Batting Statistics")
            bat_resp = requests.get(url_batting.format(player_id=player_id), headers=headers)
            if bat_resp.status_code == 200:
                bat_data = bat_resp.json()
                if "headers" in bat_data and "values" in bat_data:
                    table_header = bat_data['headers']
                    batting_stats = []
                    for row_data in bat_data['values']:
                        row = {}
                        for i, value in enumerate(row_data['values']):
                            row[table_header[i]] = value
                        batting_stats.append(row)

                    df = pd.DataFrame(batting_stats)
                    st.table(df)

#Bawling 
        with Bowling:
            st.subheader("🎯 Bowling Statistics")
            bowl_resp = requests.get(url_bowling.format(player_id=player_id), headers=headers)
            if bowl_resp.status_code == 200:
                bowl_data = bowl_resp.json()
                if "headers" in bowl_data and "values" in bowl_data:
                    table_header = bowl_data['headers']
                    bowling_stats = []
                    for row_data in bowl_data['values']:
                        row = {}
                        for i, value in enumerate(row_data['values']):
                            row[table_header[i]] = value
                        bowling_stats.append(row)

                    df = pd.DataFrame(bowling_stats)
                    st.table(df)
            else:
                st.error("Error fetching player details.")  
