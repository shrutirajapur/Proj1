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

st.header("***CRUD Operation***")
st.subheader("Create, Read, Update and Delete player records.")

crud_list=['Create','Read','Update','Delete']

select_opr=st.selectbox('Select Operation',crud_list)

if select_opr=="Read":
    st.header("View All Players")
    if st.button("Load All player"):
        select_query ="""select * from player_details;"""
        cur.execute(select_query)
        rows = cur.fetchall()   
        if rows:
            df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
            st.dataframe(df)
        else:
            st.warning("No records found.")

#Create add player
if select_opr=="Create":
    st.header("Add New Player")
    col1,col2,col3=st.columns([3,3,3])
    with col1:
        id = st.number_input('id', min_value=1, step=1)
    with col2:
        name = st.text_input('name', placeholder="e.g Virat Kohli")
    
    with col3:
        teamname = st.text_input("teamname", placeholder="e.g India") 

        #add player details
    if st.button("Add Player"):
    

        if not name.strip():
            st.error("❌ Player Name cannot be empty.")
        elif teamname is None or id is None :
            st.error("❌ All fields must be filled in.")
        else:
            
            check_query = "select * from player_details where id = %s"
            cur.execute(check_query, (id,))
            existing = cur.fetchone()
            
            if existing:
                st.warning(f"⚠️ Player with ID {id} already exists!")
            else:
                add_query = """
                    INSERT INTO player_details (id, name, teamname)
                    VALUES (%s, %s, %s)
                """
                cur.execute(add_query, (id, name, teamname))
                conn.commit()
                st.success(f"✅ Player {name} added successfully!")
                st.balloons()
#update
if select_opr == "Update":
    st.header("✏️ Update Player Record")

    id = st.number_input("Enter Player ID to update:")

    if st.button("Fetch Player"):

        select_player = "SELECT * FROM player_details  WHERE id=%s"
        cur.execute(select_player, (id,)) 
        existing = cur.fetchone() 

        if not existing:
            st.warning("⚠️ Player id does not exist.")
        
        else:
            st.session_state['selected_player']=existing 
    if 'selected_player' in st.session_state:
            existing_id, existing_name, existing_teamname = st.session_state['selected_player']
            col1, col2,col3 = st.columns([3, 3,3])
            with col1:
                new_id= st.number_input("Id", min_value=1,  value=existing_id)
               
            with col2:
                 new_name = st.text_input("Player_Name", value=existing_name)

            with col3:
                new_teamname = st.text_input("teamname",  value=existing_teamname)
                
            if st.button("Update Player",key="update_player_btn"):
                update_query = """UPDATE player_details SET name = %s WHERE id = %s"""
                cur.execute(update_query, (new_name, id))
                conn.commit()

                st.success(f"✅ name {new_name} (id: {id}) updated successfully!") 
                st.balloons()  



#delete

if select_opr == "Delete":
    st.header("🗑️ Delete Player Record")
    st.warning("⚠️ This action cannot be undone!")

    # Step 1: Search Player
    search_name = st.text_input("🔍 Search player to delete:")

    if search_name:
        search_query = "SELECT id, name, teamname FROM player_details WHERE name LIKE %s"
        search_query=search_query.strip()
        cur.execute(search_query, ("%" + search_name + "%",))
        results = cur.fetchall()

        if results:
            # Step 2: Select Player
            player_options = [f"{row[1]} (ID: {row[0]}) - {row[2]} name" for row in results]
            selected = st.selectbox("⚠️ Select player to DELETE:", player_options)

            # Extract id and name
            selected_index = player_options.index(selected)
            id, name, teamname = results[selected_index]

            st.error(f"🚨 You are about to delete: {name}")

            # Step 3: Final Confirmation
            
            confirm_text = st.text_input(f"Type 'DELETE {name}' to confirm:") 

            #if confirm_text == f"DELETE {name}":
            if st.button("✅ Confirm Delete"):
                    delete_query = "DELETE FROM player_details WHERE name = %s"
                    cur.execute(delete_query, (name,))
                    conn.commit()
                    st.success(f"✅ Player {name} deleted successfully!")
            else:
                    st.info("Type the confirmation text exactly to enable delete.")
        else:
            st.warning("No players found with that name.") 
            
            
            