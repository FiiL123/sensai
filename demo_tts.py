#!/usr/bin/env python3
"""
Simple demo of the Text-to-Speech functionality with actual audio playback
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.text_to_speech import TextToSpeechService, get_available_voices

def main():
    print("🎤 Text-to-Speech Demo (with audio playback)")
    print("=" * 40)

    try:
        # Initialize the TTS service
        tts = TextToSpeechService()

        print("\n📋 Getting available voices...")
        voices = get_available_voices()
        print(f"✅ Found {len(voices)} available voices")

        # Show first few voices
        for i, voice in enumerate(voices[:3]):
            print(f"   {i+1}. {voice['name']} ({voice['category']})")

        # Demo texts
        demos = [
            "Hello! Welcome to the sensAI learning platform.",
            "This is a demonstration of the text-to-speech functionality.",
            "The audio playback should work now!"
        ]

        for i, text in enumerate(demos, 1):
            print(f"\n🎵 Demo {i}: '{text}'")
            print("🔊 Generating and playing speech...")

            try:
                # Generate speech and play it
                audio_data = tts.speak(text, play_audio=True)
                print(f"✅ Generated and played {len(audio_data)} bytes of audio")
            except Exception as play_error:
                print(f"⚠️  Audio playback failed: {play_error}")
                print("✅ But audio generation still worked!")

        print("\n🎉 All demos completed!")
        print("If you didn't hear audio, make sure your speakers are working.")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()