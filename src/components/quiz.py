import logging
import os
import time

import streamlit as st
from dotenv import load_dotenv
from zai import ZaiClient


class QuizInterfaceClass:
    def __init__(self):
        load_dotenv()

        # Generate dynamic questions using z.ai if not already generated
        if "quiz_questions" not in st.session_state:
            self.generate_questions()

        # Initialize session state
        if "current_question" not in st.session_state:
            st.session_state.current_question = 0
            st.session_state.quiz_answers = []

        self.display_question()

    def generate_questions(self):
        """Generate 6 crucial yes/no questions using z.ai based on the topic"""
        topic = st.session_state.get("topic", "this subject")

        prompt = f"""Generate 6-8 diagnostic yes/no questions for a beginner learning about "{topic}".

        Questions should progress from general to specific, covering these levels of specificity:
        1. General awareness and interest level in {topic}
        2. Basic familiarity with fundamental {topic} concepts
        3. Experience with tools or methods commonly used in {topic}
        4. Specific knowledge of {topic} terminology and jargon
        5. Hands-on experience with practical {topic} applications
        6. Advanced understanding of {topic} concepts or methodologies

        Return only the questions, one per line, starting each with a number (1-X).
        Ensure questions flow from broad to specific assessment.
        Generate at least 6 but no more than 8 questions depending on the complexity of {topic}."""

        try:
            
            # Use z.ai SDK to generate questions
            client = ZaiClient(api_key=os.getenv("ANTHROPIC_AUTH_TOKEN"))
            
            response = client.chat.completions.create(
                model="glm-4.5",
                messages=[{"role": "user", "content": prompt}],
                thinking={
                    "type": "enabled",
                },
                max_tokens=4096,
                temperature=0.6,
            )

            
            content = response.choices[0].message.content
            

            # Enhanced parsing with multiple fallback strategies
            

            # Try different parsing strategies
            questions = []

            # Strategy 1: Parse numbered questions
            lines = content.strip().split("\n")
            

            for line in lines:
                line = line.strip()
                if line:
                    # Check if line starts with a number (e.g., "1.", "1. Question", etc.)
                    if any(char.isdigit() for char in line[:3]):
                        # Extract question after the number
                        parts = line.split(".", 1)
                        if len(parts) > 1:
                            question = parts[1].strip()
                        else:
                            question = line.strip()

                        # Clean up question
                        question = question.strip(" \"'")
                        if question and not question.endswith("?"):
                            question += "?"
                        if question:
                            questions.append(question)

            # Strategy 2: If no numbered questions found, look for question marks
            if not questions:
                
                potential_questions = [line.strip() for line in lines if line.strip().endswith("?")]
                questions.extend(potential_questions[:8])  # Take up to 8 questions

            # Strategy 3: If still no questions, split by common separators
            if not questions:
                
                sentences = []
                for line in lines:
                    if line.strip():
                        # Split by common question endings
                        parts = line.split(["?", "？", ".", "。"])
                        for part in parts:
                            part = part.strip()
                            if part and len(part) > 10:  # Reasonable length for a question
                                sentences.append(part + "?")

                questions.extend(sentences[:8])

            # Ensure we have at least 3 questions, pad if needed
            while len(questions) < 3:
                questions.append(f"Do you have any prior knowledge about {topic}?")

            # Limit to maximum 8 questions
            questions = questions[:8]

            
            

            # Validate questions
            valid_questions = []
            for q in questions:
                if len(q.strip()) > 5 and "?" in q:  # Basic validation
                    valid_questions.append(q.strip())

            if not valid_questions:
                
                valid_questions = [
                    f"Do you have any prior knowledge about {topic}?",
                    "Have you studied related subjects before?",
                    f"Are you comfortable with basic concepts in {topic}?",
                ]

            st.session_state.quiz_questions = valid_questions
            

        except Exception as e:
            
            
            # Log the error
            logging.error(f"Failed to generate questions via z.ai API: {e}")
            # Fallback to hardcoded questions if API fails
            fallback_questions = [
                f"Do you have any prior knowledge about {topic}?",
                "Have you studied related subjects before?",
                f"Are you comfortable with basic concepts in {topic}?",
                "Do you prefer visual learning over text-based learning?",
                "Have you used online learning platforms before?",
                "Are you interested in hands-on practice along with theory?",
            ]
            st.session_state.quiz_questions = fallback_questions
            

    def display_question(self):
        current_idx = st.session_state.current_question
        total_questions = len(st.session_state.quiz_questions)

        

        # Progress bar
        progress = (current_idx + 1) / total_questions
        st.progress(progress)
        st.markdown(f"**Question {current_idx + 1} of {total_questions}**")

        # Single question display
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem;
                border-radius: 15px;
                margin: 2rem 0;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            ">
                <h2 style="color: white; text-align: center; font-size: 1.8rem; margin-bottom: 1.5rem;">
                    {st.session_state.quiz_questions[current_idx]}
                </h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Yes/No buttons
        col1, col2, col3 = st.columns([2, 1, 2])

        with col1:
            if st.button("✅ Yes", use_container_width=True, type="primary"):
                self.save_answer(True)
                if current_idx < len(st.session_state.quiz_questions) - 1:
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    self.complete_quiz()

        with col3:
            if st.button("❌ No", use_container_width=True):
                self.save_answer(False)
                if current_idx < len(st.session_state.quiz_questions) - 1:
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    self.complete_quiz()

    def save_answer(self, answer):
        st.session_state.quiz_answers.append(answer)

        # Add a subtle animation effect
        if len(st.session_state.quiz_answers) < len(st.session_state.quiz_questions):
            st.success("✅ Answer saved! Moving to next question...")
            time.sleep(0.5)

    def complete_quiz(self):
        # Save both questions and answers to session for later use in learning path generation
        st.session_state.quiz_data = {
            "topic": st.session_state.get("topic", "this subject"),
            "questions": st.session_state.quiz_questions.copy(),
            "answers": st.session_state.quiz_answers.copy(),
        }
        st.session_state.current_page = "learning_path"
        st.rerun()


def QuizInterface():
    QuizInterfaceClass()
