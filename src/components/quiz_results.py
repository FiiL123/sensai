import streamlit as st
import time
import random

class QuizResultsInterfaceClass:
    def __init__(self):
        self.quiz_questions = [
            {
                "question": "What is the main purpose of machine learning?",
                "type": "multiple_choice",
                "options": ["To replace human intelligence", "To learn from data and make predictions", "To store information", "To process data faster"],
                "correct_answer": "To learn from data and make predictions",
                "explanation": "Machine learning algorithms learn patterns from data to make predictions or decisions without being explicitly programmed."
            },
            {
                "question": "Describe one concept you learned about " + st.session_state.topic + " in your own words.",
                "type": "open_ended",
                "correct_answer": None,
                "explanation": "This is an open-ended question that will be evaluated based on the completeness and accuracy of your understanding."
            },
            {
                "question": "How would you apply what you learned to solve a real-world problem?",
                "type": "open_ended",
                "correct_answer": None,
                "explanation": "Think about practical applications and how the concepts you learned can be used in real scenarios."
            }
        ]

        self.display_results()

    def display_results(self):
        st.title("🎯 Final Quiz Results")

        # Progress indicator
        progress = 1.0  # Completed learning journey
        st.progress(progress)
        st.markdown("**Congratulations on completing your learning journey!**")

        # Learning summary
        st.markdown("---")
        self.display_learning_summary()

        # Quiz questions
        st.markdown("---")
        self.display_quiz()

        # Feedback section
        st.markdown("---")
        self.display_feedback()

        # Action buttons
        st.markdown("---")
        self.display_action_buttons()

    def display_learning_summary(self):
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem;
                border-radius: 15px;
                margin: 1rem 0;
                color: white;
            ">
                <h2 style="text-align: center; margin-bottom: 1rem;">📊 Your Learning Summary</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; text-align: center;">
                    <div>
                        <h3 style="font-size: 2rem;">6</h3>
                        <p>Topics Covered</p>
                    </div>
                    <div>
                        <h3 style="font-size: 2rem;">45min</h3>
                        <p>Learning Time</p>
                    </div>
                    <div>
                        <h3 style="font-size: 2rem;">💯</h3>
                        <p>Progress</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    def display_quiz(self):
        st.markdown("### 📝 Final Assessment Questions")

        for i, question in enumerate(self.quiz_questions):
            st.markdown(f"#### Question {i+1}: {question['question']}")

            if question['type'] == 'multiple_choice':
                # Display multiple choice options
                for option in question['options']:
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.checkbox(option, key=f"q{i}_{option}")
                    with col2:
                        st.markdown(f"{option}")

                # Show correct answer
                with st.expander("💡 View Answer & Explanation"):
                    st.markdown(f"""
                    **Correct Answer:** {question['correct_answer']}

                    **Explanation:** {question['explanation']}
                    """)

            elif question['type'] == 'open_ended':
                user_answer = st.text_area(
                    "Your answer:",
                    key=f"q{i}_answer",
                    height=100,
                    placeholder="Type your answer here..."
                )

                # Evaluate answer (mock evaluation)
                if user_answer.strip():
                    evaluation_score = random.randint(70, 95)
                    with st.expander("💡 View AI Evaluation"):
                        st.markdown(f"""
                        **AI Evaluation Score:** {evaluation_score}/100

                        **Feedback:** Good understanding! {question['explanation']}
                        """)

    def display_feedback(self):
        st.markdown("### 🎉 Learning Achievement")

        # Mock achievements
        achievements = [
            "🏅 **Quick Learner**: Completed learning path efficiently",
            "🎯 **Focused**: Stayed engaged throughout the session",
            "💡 **Curious**: Asked thoughtful questions during learning",
            "📈 **Progress**: Demonstrated good understanding of concepts"
        ]

        for achievement in achievements:
            st.markdown(f"- {achievement}")

        # Overall feedback
        st.markdown("---")
        st.markdown(
            """
            <div style="
                background: #e8f5e8;
                padding: 1.5rem;
                border-radius: 10px;
                border-left: 5px solid #28a745;
            ">
                <h3 style="color: #28a745; margin-bottom: 0.5rem;">🌟 Excellent Work!</h3>
                <p>You've successfully completed your learning journey in <strong>{}</strong>.
                Your understanding and engagement show great potential for continued learning.
                Consider exploring advanced topics or applying your knowledge to practical projects!</p>
            </div>
            """.format(st.session_state.topic),
            unsafe_allow_html=True
        )

    def display_action_buttons(self):
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button("🔄 Start New Topic", use_container_width=True):
                st.success("Starting new learning journey...")
                st.session_state.current_page = 'topic_selection'
                st.session_state.clear()
                st.rerun()

        with col2:
            if st.button("📚 Review Topics", use_container_width=True):
                st.info("Navigating back to learning path...")
                st.session_state.current_page = 'learning_path'
                st.rerun()

        with col3:
            if st.button("📊 View Progress", use_container_width=True):
                st.info("Loading your progress dashboard...")

def QuizResultsInterface():
    interface = QuizResultsInterfaceClass()