"""
Example of how to integrate Text-to-Speech functionality into Streamlit components
"""

import streamlit as st
from src.utils.text_to_speech import TextToSpeechService, get_available_voices

def tts_component(text: str, auto_play: bool = True):
    """
    Streamlit component for text-to-speech functionality

    Args:
        text: The text to convert to speech
        auto_play: Whether to play the audio automatically
    """

    # Initialize TTS service
    if "tts_service" not in st.session_state:
        try:
            st.session_state.tts_service = TextToSpeechService()
        except ValueError as e:
            st.error(f"❌ TTS Service Error: {e}")
            return

    tts = st.session_state.tts_service

    # Get available voices
    if "available_voices" not in st.session_state:
        st.session_state.available_voices = get_available_voices()

    # Create UI
    st.subheader("🎤 Text-to-Speech")

    # Voice selection
    voice_names = [voice["name"] for voice in st.session_state.available_voices]
    selected_voice = st.selectbox(
        "Select Voice",
        voice_names,
        index=0
    )

    # Text input
    user_text = st.text_area(
        "Enter text to speak:",
        value=text,
        height=100,
        key="tts_text"
    )

    # Generate and play button
    if st.button("🔊 Generate Speech", type="primary"):
        try:
            # Find voice ID
            voice_id = None
            for voice in st.session_state.available_voices:
                if voice["name"] == selected_voice:
                    voice_id = voice["name"]
                    break

            # Generate speech
            with st.spinner("Generating speech..."):
                audio_data = tts.speak(user_text, voice=voice_id, play_audio=auto_play)

            st.success(f"✅ Speech generated ({len(audio_data)} bytes)")

            # Display audio player
            st.audio(audio_data, format="audio/mp3")

        except Exception as e:
            st.error(f"❌ Error generating speech: {e}")

def learning_content_tts(topic: str, content: str):
    """
    Enhanced TTS component for learning content

    Args:
        topic: The learning topic
        content: The content to read
    """

    st.markdown(f"### 📚 Learning: {topic}")

    # TTS component for the content
    tts_component(
        text=content,
        auto_play=False
    )

    # Display content
    with st.expander("📖 View Content", expanded=True):
        st.markdown(content)

    # Additional controls
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎵 Read Aloud", type="primary"):
            try:
                if "tts_service" in st.session_state:
                    tts_service = st.session_state.tts_service
                    audio_data = tts_service.speak(content, play_audio=True)
                    st.success("✅ Reading content aloud...")
            except Exception as e:
                st.error(f"❌ Error: {e}")

    with col2:
        if st.button("🔄 Read Again"):
            # This would implement repeat functionality
            st.info("Click 'Read Aloud' to repeat the content")

# Example usage in a Streamlit app:
if __name__ == "__main__":
    st.set_page_config(page_title="TTS Integration Demo", layout="wide")

    # Example 1: Basic TTS
    st.title("🎤 Text-to-Speech Integration Demo")

    # Basic component
    st.header("1. Basic TTS Component")
    tts_component("Hello! This is a demo of the text-to-speech functionality.")

    # Example 2: Learning content TTS
    st.header("2. Learning Content TTS")
    learning_content_tts(
        topic="Machine Learning Basics",
        content="Machine Learning is a subset of Artificial Intelligence that enables systems to learn from experience without being explicitly programmed. It involves algorithms that can identify patterns in data and make informed decisions based on those patterns."
    )