


import streamlit as st
#from streamlit_server_state import server_state, server_state_lock

import torch
import pandas as pd
import torchaudio

import matplotlib.pyplot as plt
from IPython.display import Audio
from io import BytesIO

#st.set_page_config(layout="wide")




def plot_specgram(x, sample_rate, title="Spectrogram", xlim=None):
    waveform = x.numpy()

    num_channels, num_frames = waveform.shape
    time_axis = torch.arange(0, num_frames) / sample_rate

    figure, axes = plt.subplots(num_channels, 1, figsize=(12, 6))
    if num_channels == 1:
        axes = [axes]
    for c in range(num_channels):
        axes[c].specgram(waveform[c], Fs=sample_rate)
        if num_channels > 1:
            axes[c].set_ylabel(f'Channel {c+1}')
        if xlim:
            axes[c].set_xlim(xlim)
    figure.suptitle(title)
    plt.show(block=True)
    
    return figure

def plot_multianimal(x, sample_rate,animal_common_name,other_animals):
    fig, ax = plt.subplots(1,1,figsize=(12, 6))
    ax.title.set_text('Spectrogram of sample - '+ animal_common_name)

    ax.specgram(x[0].numpy(), Fs=sample_rate)
    
    def indicator(row):
        if row['animal'] == animal_common_name:
            color = 'red'
            label = animal_common_name
        else:
            color = 'black'
            label = 'Other'
        #ax.axvline(x=row['time_in_sample'], color=row.index, cmap='Reds',linestyle='--', label=row['bird'])
        ax.axvline(x=row['timepoint'],c=color,linestyle=':', label=label)
        ax.text(x=.1+row['timepoint'],y= 12000, s=row['animal'], rotation=90, verticalalignment='center')
    
    other_animals.apply(indicator,axis = 1)
    #(yy).apply(ax.axvline)
    #ax[0].axvline(x=5)
    
    
    def legend_without_duplicate_labels(ax):
        handles, labels = ax.get_legend_handles_labels()
        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
        ax.legend(*zip(*unique))
    
    
    legend_without_duplicate_labels(ax)
    return fig
    
## Future - implement real-time predictions
# load the NN model
#model = torch.jit.load('/Sound/pann-test-other3.pt')

# Load the audio file
#uploaded_file = st.file_uploader("Choose an audio file")

# identify predictions


# graph predictions

st.set_option('deprecation.showPyplotGlobalUse', False)

@st.cache
def read_as_wav(file_path,start_time,end_time):
    x, sr = torchaudio.load(file_path, start_time, end_time)
    memfile= BytesIO()
    torchaudio.save(memfile, x, sr,format='wav')
    return (x,sr,memfile)
    
@st.cache
def read(file_path,start_time,end_time):
    x, sr = torchaudio.load(file_path, start_time, end_time)
    return (x,sr)

@st.cache
def animal_list(animals_df,prob=0.90):
    sel = (animals_df['maxprob']>prob)
    #blist = list(animals_df[sel]['bird'].unique())
    alist = animals_df[sel]['animal'].drop_duplicates().sort_values()
    #print(alist)
    return alist

# play the audio for a prediction
@st.cache
def animal_sound(animal_common_name, animals_df, num=10, prob=0.99):
    
    #print("animal = ",animal_common_name)
    sel = (animals_df['maxprob']>prob) & (animals_df['animal'] == animal_common_name)
    
    animals_selected = animals_df[sel].copy()
    
    avail_ct = animals_selected.shape[0]
    
    #sort in order starting with most probability
    animal_sorted = animals_selected.sort_values("maxprob",ascending=False)
 
    animal_data = animal_sorted[0:num]
    
    i=0

    animal_info = animal_sorted.iloc[i]
    
    
    #print("read audio")
    fn = animal_info["file"].replace('/media/HDD/Audio Recordings', '~/data/audio').replace('.flac','.opus')
    x, sr = read(fn, int((animal_info['time']-5)*48000), 10*48000)
    #x, sr, memfile = read_as_wav(b["file"], int((b['time']-5)*48000), 10*48000)
    #x, sr = torchaudio.load(b["file"], int((b['time']-5)*48000), 10*48000)
    
    
    #print("memfile save")
    
    memfile= BytesIO()
    
    #play_audio(x, sr)
    #audio_bytes = (x*32767).numpy().astype(int).tobytes()
    
    torchaudio.save(memfile, x, sr,format='wav')
    
    #print("sound bytes")
    memfile.seek(0)
    sound_bytes = memfile.read()
    del memfile
    
    #print("return")
        
    return animal_data, animal_info, sound_bytes, x, sr

@st.cache
def get_other_animals(animal_data, animals_df,prob):


    #  Show all animals in the clip
    
    file = animal_data.iloc[0]['file']
    t_start = animal_data.iloc[0]['time']-5
    t_length = 10
    
    
    sel = (animals_df['file'] == file) & (animals_df['time']>=t_start) & (animals_df['time']<t_start+t_length) & (animals_df['animal'] != 'No Call')
    
    unique_animals = animals_df[sel& (animals_df['maxprob']>=prob)  ]['animal'].unique()
    
    sel = sel & (animals_df['animal'].isin(unique_animals))
    
    other_animals = animals_df[sel][['animal','maxprob','time']].sort_values('time')
    other_animals['timepoint'] = (other_animals['time']-t_start)

    return other_animals
    

#Main starts here

def app(serverstate):
    animals_df = serverstate.animals_df
    
    top_container = st.container()
    
    mid_container = st.container()
    
    bot_container = st.container()
    
    with top_container:
        st.title('Animal sounds search engine')
        col1, col2 = st.columns(2)
    

    def slider_callback():
        st.write("Retrieving " + animal_name)        

    a_list = animal_list(animals_df,prob=0.90)

    #animal_name = st.select_slider('Select Animal Name',options=a_list,on_change=slider_callback)
    
    with col1:
        st.write("You can select from a wide variety of birds (like Common Loon, Great Horned Owl,"\
                 "Blue Jay, and others), a few mammals (Coyote, Eastern Chipmunk) and some amphibians"\
                 " (Green Frog).  The highest probability samples, as inferred by an AI audio"\
                 " classifier are returned, along with a spectrogram indicating the samples."\
                 "  This may take up to a minute, as the samples come from 15 days (360 hrs)"\
                 " of recordings.")
        animal_name = st.selectbox('Select Animal Name',options=a_list)
    #st.write("Retrieving " + animal_name)

    #prob = st.number_input('Enter Probability threshold %',min_value=30, max_value=99, value=90, step=1)/100.0
    prob = 0.75

    #if st.button('Get Sound'):
    if True:

        
        animal_data, animal_info, sound_bytes, x, sr= animal_sound(animal_name, animals_df, num=1, prob=.9)
        
        animal_address = "More info at [ebird.org](https://ebird.org/species/" + animal_info['animal_key']+')'
        
        
        with col2:
            st.markdown("### " + animal_info['animal'])
            st.metric("Probability:", str(int(animal_info["maxprob"]*100))+" %")
            st.write("**File:**",animal_info["file"])
            st.markdown(animal_address)
            
        other_animals = get_other_animals(animal_data, animals_df,prob)       


        #spect_plt = plot_specgram(x, sr, title=animal_info['bird'], xlim=None)
        spect_plt = plot_multianimal(x, sr,animal_info['animal'],other_animals)
        with mid_container:
            st.pyplot(fig=spect_plt)

            st.audio(sound_bytes,'audio/wav')
            st.write('** Data Points **')
            st.write(other_animals[['timepoint','animal','maxprob']])
            
        #with bot_container:
            #st.write("Finished Run")

#find_sound_app()
