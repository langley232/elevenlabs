import streamlit as st
import requests
import os
import tempfile
from pathlib import Path
import json
from datetime import datetime

# API configuration
API_URL = "http://api:8000"  # Docker service name

# Page config
st.set_page_config(
    page_title="TTS/STT Demo",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mobile responsiveness
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        margin: 5px 0;
    }
    .stTextInput>div>div>input {
        width: 100%;
    }
    @media (max-width: 768px) {
        .stApp {
            padding: 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)


def get_voices():
    try:
        response = requests.get(f"{API_URL}/voices")
        return response.json()["voices"]
    except Exception as e:
        st.error(f"Error fetching voices: {str(e)}")
        return []


def text_to_speech(text, voice_id):
    try:
        response = requests.post(
            f"{API_URL}/tts",
            json={"text": text, "voice_id": voice_id}
        )
        return response.json()
    except Exception as e:
        st.error(f"Error in TTS conversion: {str(e)}")
        return None


def save_audio(audio_path, text):
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tts_output_{timestamp}.mp3"
    output_path = output_dir / filename

    # Copy the audio file
    with open(audio_path, 'rb') as src, open(output_path, 'wb') as dst:
        dst.write(src.read())

    return output_path


# Main app
st.title("🎙️ TTS/STT Demo")

# Sidebar for voice selection
st.sidebar.title("Settings")
voices = get_voices()
selected_voice = st.sidebar.selectbox(
    "Select Voice",
    options=[voice["name"] for voice in voices],
    format_func=lambda x: x
)

# Get voice ID for selected voice
voice_id = next(
    (voice["id"] for voice in voices if voice["name"] == selected_voice), None)

# TTS Section
st.header("Text to Speech")
tts_text = st.text_area("Enter text to convert to speech", height=150)

if st.button("Convert to Speech"):
    if tts_text and voice_id:
        with st.spinner("Converting text to speech..."):
            result = text_to_speech(tts_text, voice_id)
            if result and "audio_path" in result:
                # Save the audio file
                saved_path = save_audio(result["audio_path"], tts_text)

                # Display audio player
                st.audio(str(saved_path))

                # Download button
                with open(saved_path, "rb") as f:
                    st.download_button(
                        label="Download Audio",
                        data=f,
                        file_name=saved_path.name,
                        mime="audio/mp3"
                    )
    else:
        st.warning("Please enter text and select a voice")

# STT Section
st.header("Speech to Text")
st.info("Note: STT functionality is currently a placeholder as ElevenLabs doesn't provide a direct STT API.")

# File uploader for audio files
uploaded_file = st.file_uploader(
    "Upload audio file for STT", type=["wav", "mp3"])

if uploaded_file is not None:
    st.audio(uploaded_file)
    if st.button("Convert to Text"):
        st.warning(
            "STT functionality will be implemented soon. Consider using services like Whisper API or Google Speech-to-Text.")
