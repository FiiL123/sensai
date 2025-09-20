import streamlit as st
import logging
import os
import time
import streamlit as st
from dotenv import load_dotenv
from zai import ZaiClient


class LearningPathInterfaceClass:
    def __init__(self):
        load_dotenv()
        self.generate_learning_path()
        self.display_graph()

    def generate_learning_path(self):
        # Get quiz data from session state
        if "quiz_data" not in st.session_state:
            # Fallback if no quiz data available
            topic = st.session_state.get("topic", "this subject")
            self.generate_generic_learning_path(topic)
            return

        quiz_data = st.session_state.quiz_data
        topic = quiz_data["topic"]
        questions = quiz_data["questions"]
        answers = quiz_data["answers"]

        # Calculate knowledge level based on yes answers
        yes_count = sum(1 for answer in answers if answer)
        knowledge_level = yes_count / len(answers) if answers else 0.5

        # Generate personalized learning path using z.ai
        self.generate_personalized_path(topic, questions, answers, knowledge_level)

    def generate_personalized_path(self, topic, questions, answers, knowledge_level):
        """Generate learning path based on user's knowledge level and quiz responses"""
        try:
            # Build context based on quiz answers
            yes_questions = [q for q, a in zip(questions, answers) if a]
            no_questions = [q for q, a in zip(questions, answers) if not a]

            prompt = f"""Generate a personalized learning path for someone learning about "{topic}".

            The user's knowledge level: {knowledge_level:.2f} (0.0 = beginner, 1.0 = expert)

            Questions they answered YES to (their strengths):
            {chr(10).join(f"- {q}" for q in yes_questions[:3])}

            Questions they answered NO to (their weaknesses):
            {chr(10).join(f"- {q}" for q in no_questions[:3])}

            Based on this assessment, generate exactly 4-6 subtopics that:
            1. Start with fundamentals they need to learn first
            2. Progress gradually to more advanced topics
            3. Focus on areas where they indicated weakness
            4. Build upon areas where they indicated strength
            5. Are specific and practical for {topic}

            Return only the subtopics, one per line, numbered 1-6."""

            # Use z.ai to generate personalized learning path
            client = ZaiClient(api_key=os.getenv("ANTHROPIC_AUTH_TOKEN"))
            response = client.chat.completions.create(
                model="glm-4.5", messages=[{"role": "user", "content": prompt}], max_tokens=2000, temperature=0.7
            )

            content = response.choices[0].message.content

            # Parse the response
            subtopics = []
            lines = content.strip().split("\n")

            for line in lines:
                line = line.strip()
                if line and any(char.isdigit() for char in line[:3]):
                    # Extract topic after the number
                    parts = line.split(".", 1)
                    if len(parts) > 1:
                        topic_name = parts[1].strip()
                        if topic_name:
                            subtopics.append(topic_name)

            if not subtopics:
                # Fallback to generic generation
                self.generate_generic_learning_path(topic)
            else:
                st.session_state.learning_path = subtopics[:6]  # Limit to 6 topics

        except Exception as e:
            logging.error(f"Failed to generate personalized learning path: {e}")
            self.generate_generic_learning_path(topic)

    def generate_generic_learning_path(self, topic):
        """Generate a generic learning path as fallback"""
        subtopics = [
            f"Introduction to {topic}",
            f"Basic Concepts of {topic}",
            f"Core Principles of {topic}",
            f"Intermediate Topics in {topic}",
            f"Advanced Concepts of {topic}",
            f"Practical Applications of {topic}",
            f"Tools and Methods for {topic}",
            f"Best Practices in {topic}",
            f"Real-world Examples of {topic}",
            f"Future Trends in {topic}",
        ]
        st.session_state.learning_path = subtopics[:8]

    def display_graph(self):
        st.title("🗺️ Your Personalized Learning Path")

        # Get quiz data for knowledge level display
        if "quiz_data" in st.session_state:
            quiz_data = st.session_state.quiz_data
            answers = quiz_data["answers"]
            yes_count = sum(1 for answer in answers if answer)
            knowledge_level = yes_count / len(answers) if answers else 0.5

            # Progress indicator
            progress = 0.6  # Quiz completed, now at learning path
            st.progress(progress)

            # Knowledge level summary
            st.markdown("### **Your Knowledge Assessment**")
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                st.metric("Answered Yes", f"{yes_count}/{len(answers)}")

            with col2:
                st.metric("Knowledge Level", f"{knowledge_level:.1%}")

            with col3:
                level_text = (
                    "Beginner" if knowledge_level < 0.3 else "Intermediate" if knowledge_level < 0.7 else "Advanced"
                )
                st.metric("Level", level_text)

            st.markdown("---")
            st.markdown("**Based on your assessment, here's your personalized learning path:**")
        else:
            st.markdown("**Here's your learning path:**")

        # Create the enhanced graph
        self.create_interactive_graph()

        # Instructions
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; margin-top: 2rem;">
                <p style="font-size: 1.1rem; color: #666;">
                    👆 Click on any topic node to start learning
                </p>
                <p style="font-size: 1.1rem; color: #666;">
                    🔄 Topics are arranged from fundamentals to advanced concepts
                </p>
                <p style="font-size: 1.1rem; color: #666;">
                    🎯 Focus on areas where you need more practice
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    def create_interactive_graph(self):
        learning_path = st.session_state.learning_path

        # Add clickable buttons for each node below the chart
        st.markdown("---")
        st.markdown("### **Click on a topic to start learning:**")

        # Create columns for the topic buttons
        cols = st.columns(len(learning_path))

        for i, topic in enumerate(learning_path):
            with cols[i]:
                if st.button(
                    topic,
                    key=f"node_{i}",
                    use_container_width=True
                ):
                    st.session_state.current_slide = topic
                    st.session_state.current_page = 'slide_display'
                    st.rerun()

def LearningPathInterface():
    interface = LearningPathInterfaceClass()
