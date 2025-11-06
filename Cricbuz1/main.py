import streamlit as st 
import Cricbuz.Pages.Live as Live
import Cricbuz.Pages.PlayerStats as PlayerStats
import Cricbuz.Pages.CRUD as CRUD
import Cricbuz.Pages.SQL_Queries as SQL_Queries

st.sidebar.title("Navigation")
option=st.sidebar.selectbox("Select the page.. ",["Live Matches",   "Player Stats", "CRUD Operations","SQL Queries"])


st.title("🏏 Cricbuzz  Dashboard")
    
if option == "Live Matches":
     Live.app()

elif option=="Player Stats":
     PlayerStats.app()
  
elif option=='CRUD Operations':
     CRUD.app()
  

elif option=="SQL Queries":
    SQL_Queries.app()

    
    
