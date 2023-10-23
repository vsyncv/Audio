import os
import streamlit as st
from gtts import gTTS
from pydub import AudioSegment

def synthesize_text(text, language):
    try:
        if text:
            tts = gTTS(text=text, lang=language)
            return tts.save("temp.mp3")
    except Exception as e:
        st.error("Error occurred during text synthesis.")

def process_audio_file(filename):
    try:
        audio = AudioSegment.from_file(filename)

                # Modify the audio speed
        if speed > 1:
            audio = audio.speedup(playback_speed=speed)
        elif speed < 1:
            audio = audio.slowdown(playback_speed=speed)

        # Modify the audio as needed (e.g., convert to mono, adjust volume, remove silent sections)
        # Add your audio processing logic here

        # Export the processed audio as WAV with 8-bit encoding
        processed_filename = os.path.splitext(filename)[0] + '_processed.wav'
        audio.export(processed_filename, format='wav', parameters=['-f', 'wav', '-ac', '1', '-ar', '11025', '-acodec', 'pcm_u8'])
        print(f'Processed audio file saved: {processed_filename}')
        return processed_filename
    except Exception as e:
        st.error("Error occurred during audio processing.")

# Set the default announcement text and language
default_text = ""
default_language = 'en'  # English

# Create input fields for announcement text, language, and speed
announcement_text = st.text_input("Enter Announcement Text", default_text)
language = st.selectbox("Select Language", ['en', 'fr', 'es'], index=0)
speed = st.slider("Select Speed", min_value=0.5, max_value=2.0, step=0.1, value=1.0)


# Synthesize text to speech
synthesize_text(announcement_text, language)

# Process the audio file
processed_filename = process_audio_file("temp.mp3")

if processed_filename:
    # Display an audio player for the processed audio file
    st.audio(processed_filename, format='audio/wav')
