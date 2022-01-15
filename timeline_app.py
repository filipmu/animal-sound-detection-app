import streamlit as st
from streamlit_timeline import timeline
import pandas as pd


date = {'year':2020,
        'month':12,
        'day':25}

title = {'text':{'headline':"My Recordings", 'text':'a timeline'}}

slide = {'start_date':{'year':2021,'month':6,'day':1,'hour':1,'minute':1},
         'end_date':{'year':2021,'month':6,'day':1,'hour':1,'minute':2},
         'text':{'headline':"My Animal", 'text':'a bird'}}
era ={'start_date':{'year':2020,'month':12,'day':25},
      'end_date':{'year':2021,'month':12,'day':6},
      'text':{'headline':"Filename", 'text':'file'}}




data = {'events':[slide],
        'title': title,
        'eras': [era],
        'scale':'human'}



def app(serverstate):
    timeline_dict = serverstate.timeline_dict
    
    top_container = st.container()
    
    mid_container = st.container()
    
    bot_container = st.container()
    
    with top_container:
        st.title('Recording timelines - draft')
        
        
    
    #st.json(timeline_dict)
    
    with mid_container:
        timeline(timeline_dict, height=800)
    