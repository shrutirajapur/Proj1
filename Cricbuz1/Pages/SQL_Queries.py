import streamlit as st
import pandas as pd
import psycopg2

conn = psycopg2.connect(
    host = "localhost",
    port = 5432,
    dbname = "Cricbuzz_project ",
    user = "postgres",
    password = "Direction@12")

cur = conn.cursor()


queries={

"Find all players who represent India. Display their full name, playing role, batting style, and bowling style":
'''select PS.name,PS.role,PS.battingstyle,PS.bowlingstyle
from playing_style as PS
inner join player_details as PD 
on PD.id=PS.id
where PS.id=576;''',

"Show all cricket matches that were played in the last Few days. Include the match description, both team names, venue name with city, and the match date. Sort by most recent matches first.":

'''select matchdesc,teamname1,teamname2,ground,city,startdate,enddate 
from series_matches
order by startdate desc;''',

"List the top 10 highest run scorers in ODI cricket. Show player name, total runs scored, batting average, and number of centuriesDisplay the highest run scorer first":

'''select ML.matchid,ML.matchformat,ML.teamname1,ML.teamname2,MS.runs,MS.overs from matchscore as MS
left join match_list as ML 
on ML.matchid=MS.matchid
where ML.matchformat='ODI' order by runs desc;''',

"Display all cricket venues that have a seating capacity of more than 30,000 spectators. Show venue name, city, country, and capacity. Order by largest capacity first":
'''select * from venue where capacity >10000;''',

"Calculate how many matches each team has won. Show team name and total number of wins. Display teams with the most wins first.":

'''SELECT 
    seriesId, 
    teamname1, 
    teamname2, 
    COUNT(*) AS MatchesWon 
FROM 
    match_list 
GROUP BY 
    seriesId, teamname1, teamname2 
ORDER BY 
    MatchesWon DESC;''',

"Count how many players belong to each playing role (like Batsman, Bowler, All-rounder, Wicket-keeper). Show the role and count of players for each role.":
'''SELECT battingstyle,bowlingstyle,role,count(*) as playing_style
from playing_style
group by battingstyle,bowlingstyle,role
order by playing_style desc;''',
	
"Find the highest individual batting score achieved in each cricket format (Test, ODI, T20I). Display the format and the highest score for that format":

'''select match_type, runs,balls,highest 
from batting_details
order by runs desc;''',

"Show all cricket series that started in the year 2024. Include series name, host country, match type, start date, and total number ofmatches planned.":


'''select * from series_details where startdt='1707955200000';''',

"--- Find all-rounder players who have scored more than 1000 runs AND taken more than 50 wickets in their career. Display player name,total runs, total wickets, and the cricket format.":

'''select max(MD.role) as Allrounder,MD.batteamid ,max(MD.name) as name,sum(MD.runs) as Runs ,Sum(MD.overs) as Overs
from match_details as MD
join playing_style as PS on MD.role = PS.role
where MD.role in ('Batting Allrounder' , 'Bowling Allrounder' )
group by MD.batteamid;''',


"10 Show match description, both team names, winning team, victory margin, victory type (runs/wickets), and venue name. Display most recent matches first.":

'''select ML.matchdesc,ML.teamname1,ML.teamname2,ML.statetitle,ML.state,ML.ground,s.run1,s.wicket1,s.run2,s.wicket2
from match_list as ML
join score as s
on ML.matchid=s.match_id
order by enddate desc;''',

"Question 11 Compare each player's performance across different cricket formats. For players who have played at least 2 different formats show their total runs in Test cricket, ODI cricket, and T20I cricket, along with their overall batting average across all formats":

'''select s.series_id,max(ML.matchdesc) as MatchDesc,max(ML.matchformat) as Format,sum(s.run1) as total_run1,
sum(s.run2) as total_run2
from match_list as ML
join score as s
on ML.seriesid=s.series_id
group by s.series_id;''',

"---Question 12 Analyze each international team's performance when playing at home versus playing away. Determine whether each team played at home or away based on whether the venue country matches the team's country. Count wins for each team in both home and away conditions.":

'''SELECT 
    teamname1,
    CASE
        WHEN country = teamname1 THEN 'HOME'
        ELSE 'AWAY'
    END AS Match_Type,
    COUNT(*) AS Total_Wins
FROM schedule_list
WHERE country =teamname or country=teamname1
GROUP BY teamname1, Match_Type
ORDER BY teamname1, Match_Type;''',


}
st.header("Select  a query from list")

selected_query = st.selectbox("Select Query", queries.keys())

if st.button("Run Query", key="run_query_btn"):
    cur.execute(queries[selected_query])
    result = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    df = pd.DataFrame(result, columns=columns)
    st.dataframe(df)

conn.close() 