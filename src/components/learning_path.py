import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
import time

class LearningPathInterfaceClass:
    def __init__(self):
        self.generate_learning_path()
        self.display_graph()

    def generate_learning_path(self):
        # Mock learning path based on topic and quiz answers
        topic = st.session_state.topic

        # Generate sub-topics based on the main topic
        if "machine learning" in topic.lower():
            subtopics = [
                "Introduction to Machine Learning",
                "Supervised Learning Basics",
                "Unsupervised Learning Concepts",
                "Neural Networks Fundamentals",
                "Deep Learning Overview",
                "Model Evaluation & Validation"
            ]
        elif "python" in topic.lower():
            subtopics = [
                "Python Syntax Basics",
                "Data Structures in Python",
                "Functions and Modules",
                "Object-Oriented Programming",
                "Python Standard Library",
                "Advanced Python Concepts"
            ]
        else:
            # Generic learning path structure
            subtopics = [
                f"Introduction to {topic}",
                f"Basic Concepts of {topic}",
                f"Core Principles of {topic}",
                f"Advanced Topics in {topic}",
                f"Practical Applications of {topic}",
                f"Future of {topic}"
            ]

        st.session_state.learning_path = subtopics

    def display_graph(self):
        st.title("🗺️ Your Personalized Learning Path")

        # Progress indicator
        progress = 0.6  # Quiz completed, now at learning path
        st.progress(progress)
        st.markdown("**Based on your answers, here's your learning path:**")

        # Create the graph
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
                    🔄 Topics are arranged in recommended order
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
