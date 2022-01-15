#https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4

# A Streamlit app
# streamlit run app.py &

#run localtunnel to expose on internet for testing purposes
# lt --subdomain animal-sounds --port 8501 &

import streamlit as st
from pathlib import Path
import pandas as pd
import json

import find_sound_app
import timeline_app

from streamlit_server_state import server_state, server_state_lock

st.set_page_config(page_title="nature-sounds",layout="wide")

#load the predicted data
results_path = Path('/home/user/streamlit-apps')

@st.cache
def load_data(results_path):
    animals_df = pd.read_csv(results_path/ 'cabin_birds_df.csv',index_col=[0])
    animals_df.rename(columns ={'bird':'animal', 'bird_key':'animal_key'},inplace=True)
    
    return animals_df

with server_state_lock["animals_df"]:
    if "animals_df" not in server_state:
        server_state.animals_df = load_data(results_path)

animals_df = server_state.animals_df

@st.cache
#def load_filelist(results_path):
#    files_df = pd.read_csv(results_path/ 'cabin_files_df.csv',index_col=[0])
#    return files_df

#with server_state_lock["files_df"]:
#    if "files_df" not in server_state:
#        server_state.files_df = load_filelist(results_path)

#files_df = server_state.files_df

@st.cache
def load_timeline(results_path):
    with open(results_path/ 'cabin_timeline.json') as data_file:
        timeline_dict = json.load(data_file)      
    return timeline_dict

with server_state_lock["timeline_dict"]:
    if "timeline_dict" not in server_state:
        server_state.timeline_dict = load_timeline(results_path)

timeline_dict = server_state.timeline_dict







pages = {
    "Find a Sound":find_sound_app,
    "See Timeline":timeline_app
    }



with st.sidebar.title('Navigation'):
    selection = st.radio("Go to",list(pages.keys()))
    page = pages[selection]


page.app(server_state)
    
