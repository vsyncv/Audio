import os
import streamlit as st
from gtts import gTTS
from pydub import AudioSegment

class TextToSpeechApp:
    def __init__(self):
        self.default_text = ""
        self.default_language = 'en'  # English
        self.temp_file = "temp.mp3"

    def synthesize_text(self, text: str, language: str) -> None:
        try:
            if text:
                tts = gTTS(text=text, lang=language)
                tts.save(self.temp_file)
        except Exception as e:
            st.error(f"Error occurred during text synthesis: {e}")

    def process_audio_file(self, filename: str, speed: float) -> str:
        try:
            audio = AudioSegment.from_file(filename)
            audio = self.adjust_audio_speed(audio, speed)
            
            # Further audio processing can be added here

            # Exporting the processed audio
            processed_filename = os.path.splitext(filename)[0] + '_processed.wav'
            audio.export(processed_filename, format='wav', parameters=['-f', 'wav', '-ac', '1', '-ar', '11025', '-acodec', 'pcm_u8'])
            return processed_filename
        except Exception as e:
            st.error(f"Error occurred during audio processing: {e}")
            return None

    @staticmethod
    def adjust_audio_speed(audio: AudioSegment, speed: float) -> AudioSegment:
        if speed > 1:
            return audio.speedup(playback_speed=speed)
        elif speed < 1:
            return audio.slowdown(playback_speed=speed)
        return audio

    def run(self):
        # UI components for Streamlit
        announcement_text = st.text_input("Enter Announcement Text", self.default_text)
        language = st.selectbox("Select Language", ['en', 'fr', 'es'], index=0)
        speed = st.slider("Select Speed", min_value=0.5, max_value=2.0, step=0.1, value=1.0)

        if announcement_text:
            self.synthesize_text(announcement_text, language)
            processed_filename = self.process_audio_file(self.temp_file, speed)
            if processed_filename:
                st.audio(processed_filename, format='audio/wav')


if __name__ == "__main__":
    app = TextToSpeechApp()
    app.run()
