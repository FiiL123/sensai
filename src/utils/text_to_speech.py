import os
import logging
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TextToSpeechService:
    """Service for generating and playing text-to-speech using ElevenLabs API"""

    def __init__(self, api_key=None):
        """Initialize the ElevenLabs client"""
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in environment variables")

        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        self.logger = logging.getLogger(__name__)

    def generate_speech(self, text: str, voice: str = "Rachel", model: str = "eleven_multilingual_v2") -> bytes:
        """
        Generate speech from text using ElevenLabs API

        Args:
            text: The text to convert to speech
            voice: The voice name to use (default: Rachel)
            model: The model to use (default: eleven_multilingual_v2)

        Returns:
            Audio data as bytes
        """
        try:
            self.logger.info(f"Generating speech for text: {text[:50]}...")

            # First get the voice ID by listing voices
            voices_response = requests.get(
                f"{self.base_url}/voices",
                headers=self.headers
            )
            voices_response.raise_for_status()

            voices_data = voices_response.json()
            voice_id = None
            for v in voices_data['voices']:
                if v['name'].lower() == voice.lower():
                    voice_id = v['voice_id']
                    break

            if not voice_id:
                # Use first available voice as fallback
                voice_id = voices_data['voices'][0]['voice_id']

            # Generate speech using ElevenLabs API
            tts_url = f"{self.base_url}/text-to-speech/{voice_id}"
            payload = {
                "text": text,
                "model_id": model,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }

            response = requests.post(
                tts_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()

            self.logger.info(f"Speech generated successfully. Size: {len(response.content)} bytes")
            return response.content

        except Exception as e:
            self.logger.error(f"Error generating speech: {e}")
            raise

    def play_audio(self, audio_data: bytes):
        """
        Play audio data using pygame

        Args:
            audio_data: Audio data as bytes
        """
        try:
            import pygame
            pygame.init()
            pygame.mixer.init()

            # Create a temporary file to store the audio
            temp_file = "temp_audio.mp3"
            with open(temp_file, "wb") as f:
                f.write(audio_data)

            # Load and play the audio
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()

            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)

            # Clean up
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            os.remove(temp_file)

            self.logger.info("Audio playback completed")

        except ImportError:
            self.logger.error("pygame library not installed. Install with: pip install pygame")
            raise
        except Exception as e:
            self.logger.error(f"Error playing audio: {e}")
            raise

    def speak(self, text: str, voice: str = "Rachel", play_audio: bool = True):
        """
        Generate and optionally play speech from text

        Args:
            text: The text to convert to speech
            voice: The voice name to use
            play_audio: Whether to play the audio immediately

        Returns:
            Audio data as bytes
        """
        try:
            audio_data = self.generate_speech(text, voice)

            if play_audio:
                self.play_audio(audio_data)

            return audio_data

        except Exception as e:
            self.logger.error(f"Error in speak method: {e}")
            raise


def get_available_voices():
    """Get list of available voices from ElevenLabs"""
    try:
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            raise ValueError("ELEVENLABS_API_KEY not found")

        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }

        response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)
        response.raise_for_status()

        voices_data = response.json()
        available_voices = []

        for voice in voices_data['voices']:
            available_voices.append({
                "id": voice['voice_id'],
                "name": voice['name'],
                "category": voice.get('category', 'unknown')
            })

        return available_voices

    except Exception as e:
        logging.error(f"Error getting available voices: {e}")
        return []