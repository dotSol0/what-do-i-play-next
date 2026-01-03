import streamlit as st
import pandas as pd
from pathlib import Path

# 1. Get the folder where 'streamlit.py' sits (frontend/app)

df = pd.read_csv('../../data/processed/processed-40k.csv')

import streamlit as st
import baseline.py

# Define a list of options for the dropdown
TimePeriodList = ['Baroque', 'Classical', 'Romantic', '20th century']

# Create the dropdown menu (select box)
time_period = st.selectbox(
    'How would you like to be contacted?', # The label displayed above the dropdown
    TimePeriodList                       # The list of options
)

Instrument = ['flute', 'oboe', 'clarinet', 'alto saxophone', 
              'trumpet', 'french horn', 'trombone', 'tuba', 
              'violin', 'viola', 'cello', 'string bass', 
              'piano', 'voice', 'piano 4 hands']

# Create the dropdown menu (select box)
instrument = st.multiselect(
    'What instrument do you play?', # The label displayed above the dropdown
    Instrument                    # The list of options
)

Key = ['C', 'C#/Db', 'D', 'D#/Eb', 
              'E', 'F' 'F#/Gb', 'G', 
              'G#/Ab', 'A', 'A#/Bb', 'B', 'various']

# Create the dropdown menu (select box)
key = st.multiselect(
    'What key?', # The label displayed above the dropdown
    Key                    # The list of options
)

mode = st.segmented_control('Major or minor?' , ["All", "major", "minor"])


year_range = range(1500, 2026 + 1)
year_list = list(year_range)

start_year, end_year = st.select_slider(
    "Select when your piece should be published",
    options = year_list,
    value=(1500, 2026),
)
st.write("You selected wavelengths between", start_year, "and", end_year)

duration_selection = st.segmented_control('' , ["Year", "Range"])
duration_range = range(1, 120 + 1)
duration_list = list(duration_range)

if duration_selection == "Year": 
    start_duration = st.select_slider(
        "How Long is your Piece?",
        options = duration_list
    )
    end_duration = None
elif duration_selection == "Range":
    start_duration, end_duration = st.select_slider(
    "How Long is your Piece (in minutes)?",
    options = duration_list,
    value=(1, 120),
    )
    st.write("You selected wavelengths between", start_duration, "and", end_duration)


clicked = st.button("Click to Submit")
if clicked:
    query = [time_period, instrument, key, mode, str(start_year), 
             str(end_year), str(start_duration), str(end_duration)]







