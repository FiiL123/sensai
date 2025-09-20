import streamlit as st
import time

class QuizInterfaceClass:
    def __init__(self):
        self.questions = [
            "Do you have any prior knowledge about " + st.session_state.topic + "?",
            "Have you studied related subjects before?",
            "Are you comfortable with basic concepts in this field?",
            "Do you prefer visual learning over text-based learning?",
            "Have you used online learning platforms before?",
            "Are you interested in hands-on practice along with theory?"
        ]

        if 'current_question' not in st.session_state:
            st.session_state.current_question = 0
            st.session_state.quiz_answers = []

        self.display_question()

    def display_question(self):
        current_idx = st.session_state.current_question
        total_questions = len(self.questions)

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
                    {self.questions[current_idx]}
                </h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Yes/No buttons
        col1, col2, col3 = st.columns([2, 1, 2])

        with col1:
            if st.button("✅ Yes", use_container_width=True, type="primary"):
                self.save_answer(True)
                if current_idx < len(self.questions) - 1:
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    self.complete_quiz()

        with col3:
            if st.button("❌ No", use_container_width=True):
                self.save_answer(False)
                if current_idx < len(self.questions) - 1:
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    self.complete_quiz()

    def save_answer(self, answer):
        st.session_state.quiz_answers.append(answer)

        # Add a subtle animation effect
        if len(st.session_state.quiz_answers) < len(self.questions):
            st.success("✅ Answer saved! Moving to next question...")
            time.sleep(0.5)

    def complete_quiz(self):
        st.session_state.current_page = 'learning_path'
        st.rerun()

def QuizInterface():
    quiz = QuizInterfaceClass()