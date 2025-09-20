import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.utils.text_to_speech import TextToSpeechService, get_available_voices


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def test_tts_service():
    try:
        tts_service = TextToSpeechService()

        voices = get_available_voices()

        test_text = "Hello, this is a test of the text-to-speech functionality. The service is working correctly."

        try:
            audio_data = tts_service.generate_speech(test_text)
        except Exception:
            return False

        longer_text = """
        Welcome to the sensAI learning platform. This system helps you learn various subjects
        through personalized learning paths and interactive content. Let me read this text
        to demonstrate the text-to-speech capabilities.
        """

        try:
            longer_audio = tts_service.generate_speech(longer_text)
        except Exception:
            return False

        user_input = input("\nWould you like to test audio playback? (y/n): ").lower().strip()

        if user_input == "y":
            try:
                tts_service.speak("""Welcome to the sensAI learning platform. This system helps you learn various subjects
        through personalized learning paths and interactive content. Let me read this text
        to demonstrate the text-to-speech capabilities. This is a test of the audio playback functionality.""")
            except Exception:
                pass

        try:
            invalid_tts = TextToSpeechService("invalid_api_key")
        except ValueError:
            pass
        except Exception:
            pass

        return True

    except Exception:
        return False


if __name__ == "__main__":
    setup_logging()

    if not os.getenv("ELEVENLABS_API_KEY"):
        sys.exit(1)

    success = test_tts_service()
    sys.exit(0 if success else 1)
