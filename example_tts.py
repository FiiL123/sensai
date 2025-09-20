#!/usr/bin/env python3
"""
Example usage of the Text-to-Speech service
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.text_to_speech import TextToSpeechService

def main():
    print("🎤 Text-to-Speech Example")
    print("=" * 30)

    try:
        # Initialize the TTS service
        tts = TextToSpeechService()

        # Example texts for different learning scenarios
        examples = [
            {
                "title": "Welcome Message",
                "text": "Welcome to sensAI! This is an intelligent learning platform designed to personalize your educational journey."
            },
            {
                "title": "Learning Content",
                "text": "Today we're going to explore the fascinating world of machine learning. You'll learn about algorithms, models, and how to apply them to real-world problems."
            },
            {
                "title": "Encouragement",
                "text": "Great progress! Keep up the excellent work. Remember, learning is a journey, and every step forward brings you closer to mastery."
            },
            {
                "title": "Study Break",
                "text": "Time for a short break! Remember to stay hydrated and take a moment to stretch your legs before continuing your studies."
            }
        ]

        for example in examples:
            print(f"\n📝 {example['title']}")
            print("Text:", example['text'][:50] + "...")

            choice = input("\nWould you like to hear this? (y/n): ").lower().strip()
            if choice == 'y':
                print("🔊 Generating speech...")
                audio_data = tts.speak(example['text'])
                print(f"✅ Speech generated ({len(audio_data)} bytes)")
            else:
                print("⏭️  Skipping")

        print("\n🎉 Example completed!")

    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please ensure ELEVENLABS_API_KEY is set in your .env file")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()