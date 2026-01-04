import streamlit as st
import pandas as pd
from pathlib import Path
import sys
print(sys.path)





ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.inference.recommend import baseline_query



st.title("What Should I Play Next?")
st.markdown("*What should you play for your next your next musical endeavor?*")

# 1. Get the folder where 'streamlit.py' sits (frontend/app)
@st.cache_data  # 👈 Add the caching decorator
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data('data/processed/processed-40k.csv')





# Define Variables as None
time_period = None
instrument = None
key = None
mode = None
start_year = None
end_year = None
start_duration = None
end_duration = None

# Define a list of options for the dropdown
TimePeriodList = ['none', 'baroque', 'classical', 'romantic', 'early 20th century', 'modern']

# Create the dropdown menu (select box)
time_period = st.selectbox(
    'What style of piece do you want?', # The label displayed above the dropdown
    TimePeriodList                       # The list of options
)
if time_period == 'none':
    time_period = None

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
              'E', 'F', 'F#/Gb', 'G', 
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
    
ROWS_PER_PAGE = 5

if "page" not in st.session_state:
    st.session_state.page = 0

def render_results(df, page, rows_per_page=5):
    start = page * rows_per_page
    end = start + rows_per_page

    subset = df.iloc[start:end]

    if subset.empty:
        st.info("No more results.")
        return

    for _, row in subset.iterrows():
        # map CSV columns to UI fields (fallback if names differ)
        with st.container():
            title = row.get("Title") or row.get("Name") or "Untitled"
            composer = row.get("Composer") or row.get("Author") or ""
            key = row.get("Key") or ""
            instrument = row.get("Instrumentation") or ""
            year = row.get("Year") or row.get("Year Published") or ""
            link = row.get("Permlink") or row.get("Hyperlink") or ""

            st.subheader(title)
            if composer:
                st.markdown(f"**Composer:** {composer}")
            if key:
                st.markdown(f"**Key:** {key}")
            if instrument:
                st.markdown(f"**Instrument:** {instrument}")
            if year:
                st.markdown(f"**Year Published:** {int(year)}")
            if link:
                st.markdown(f"[Open score]({link})")


clicked = st.button("Click to Submit")
if clicked:
    query = [
        time_period,
        instrument,
        key,
        mode,
        start_year,
        end_year,
        start_duration,
        end_duration
    ]

    st.session_state.results = baseline_query(query, df)
    st.session_state.page = 0  # reset pagination



if "results" in st.session_state:
    render_results(
        st.session_state.results,
        st.session_state.page,
        rows_per_page=5
    )


if "results" in st.session_state:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Previous", disabled=st.session_state.page == 0):
            st.session_state.page -= 1

    with col2:
        if st.button("Next "):
            st.session_state.page += 1






