import streamlit as st
import requests
import pandas as pd


st.title("Live Matches Dashboard")
page = st.sidebar.radio("Choose Page", ["Live"])
st.title("Select a match")
col1, col2 = st.columns([4, 1])
with col1:
    match_names = st.text_input("Available matches")
with col2:
    search_btn = st.button("Search")

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

headers = {
	"x-rapidapi-key": "bf10e75c34mshe29d2ac7bca38cep143477jsn19fd2ab2770f",
	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
data = response.json()

matches = []


for type_match in data.get("typeMatches", []):
    for series_match in type_match.get("seriesMatches", []):
        series_data = series_match.get("seriesAdWrapper", {})
        series_id = series_data.get("seriesId")
        series_name = series_data.get("seriesName")

        for match_data in series_data.get("matches", []):
            info = match_data.get("matchInfo", {})
            match_id = info.get("matchId")
            match_desc = info.get("matchDesc")
            match_format = info.get("matchFormat")
            start_date = info.get("startDate")
            status = info.get("status")
            
            team1 = info.get("team1", {}).get("teamName")
            team2 = info.get("team2", {}).get("teamName")

            venue = info.get("venueInfo", {}).get("ground")

            matches.append({
                "series_id": series_id,
                "series_name": series_name,
                "match_desc": match_desc,
                "match_format": match_format,
                "start_date": start_date,
                "status": status,
                "team1": team1,
                "team2": team2,
                "venue": venue,
                "match_id": match_id
            })

df = pd.DataFrame(matches)
st.dataframe(df)





if page == "Live":
    if not matches:
        st.warning("⚠ No live matches are currently available.")
    else:
            match_names = [f"{m['team1']} vs {m['team2']} - {m['match_desc']} ({m['status']})" for m in matches]
            selected = st.selectbox("Select Match", match_names,index=0)
            selected_match = matches[match_names.index(selected)]
            st.header(f"{selected_match['team1']} vs {selected_match['team2']}")
            st.write(f"**Series:** {selected_match['series_name']}")
            st.write(f"**Match:** {selected_match['match_desc']}")
            st.write(f"**Venue:** {selected_match['venue']}")
            st.write(f"**Status:** {selected_match['status']}")
            st.write(f"**Match ID:** {selected_match['match_id']}")

   
   