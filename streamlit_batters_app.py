
import pickle
import streamlit as st
#import sys 
#sys.path.append('C:/Users/adith/Documents/ipl_app/team_app/batting')
from batsman import Batsmant
with open('batting1.pkl', 'rb') as f:
    bat = pickle.load(f)
    #result1=bat.calculate("Sunrisers Hyderabad",[1,2,3],["Pace"],[2022])
    #print(result1['strike_rate'])

def main():
    # Title of the app
    st.title("T20 Leagues: Team Batting Stats")
    # Input for PlayerName
   
    
    team_names = bat.teams

    league_names=bat.league
    league_names = st.multiselect("Select Leagues ",league_names)
    team_name = st.selectbox("Select Team Name", team_names)
    phases = st.multiselect("Select Phases ", ["Powerplay", "Middle1","Middle2","Slog"])
    # Input for Bowling type (dropdown)
    bowling_type = st.multiselect("Select Bowling Type(s)", ["Pace", "Spin"])
    start_year = 2016
    end_year = 2023
    selected_years = st.slider("Select Seasons", start_year, end_year, (start_year, end_year))
    ph1={'Powerplay':1,'Middle1':2,'Middle2':3,'Slog':4}

    overs=[ph1[phases[i]] for i in range(len(phases))]
    bowling_type=[bowling_type[i] for i in range(len(bowling_type))]
    Season=[i for i in range(selected_years[0],selected_years[1]+1)]
    if st.button('Submit'):


        #st.write("Selected Player Name:", player_name)
        #st.write("Selected Player Name:", team_name)
        #st.write("Selected Bowling Type:", type(bowling_type[0]))  # Corrected indentation
        #st.write("Selected Phases:", len(phases))          
        #st.write("Selected Seasons:", selected_years[0], "to", selected_years[1])
        
        result1=bat.calculate(league_names,team_name,overs,bowling_type,Season)
        result2=bat.overall()
        
        
        result3=bat.combined()
        st.write("Overall (All phases and bowling types ):")
        st.dataframe(result2)
        
        st.write("Combined (Given phases and bowling types ):")
        st.dataframe(result3)


        st.write("Phase wise breakdown:")
        result1=result1.iloc[:,[7,6,0,1,2,3,4,5,8]]
if __name__ == '__main__':
    main()