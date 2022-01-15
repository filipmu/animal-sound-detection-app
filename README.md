# animal-sound-detection-app


<a href="https://github.com/filipmu/animal-sound-detection-app/blob/main/screenshot.png" target="_blank" rel="noopener noreferrer">
 <img src="https://github.com/filipmu/animal-sound-detection-app/blob/main/screenshot.png" alt="screenshot" width="200" height="200">
</a>


## What it does
A web application that allows the user to search for animal calls in over 15 days of recordings. Select the animal common name and it returns a 10 second stereo sound sample centered on the animal call.  Also shows the spectrogram of the sample, along with the location of the call and the names of any other animals and calls detected.  

## How it works
Its based on a huge look up table of all high-probability animal calls and their time stamps in the recordings.  This was created off-line using an AI sound event detection algorithm trained on bird calls and a few other calling animals (coyote, frogs, toads, chipmunk).  See https://github.com/filipmu/nature-audio-ai  

## What it uses
It uses the streamlit library in python, and is hosted on a small server with a caddy2 web server running as a reverse proxy.

## How do I try it

[Animal Sounds Search Engine](https://info.muliercloud.com/)
