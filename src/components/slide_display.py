import streamlit as st
import time

class SlideDisplayInterfaceClass:
    def __init__(self):
        self.slide_content = self.generate_slide_content()
        self.display_slide()

    def generate_slide_content(self):
        current_slide = st.session_state.current_slide
        topic = st.session_state.topic

        # Mock slide content based on current slide and topic
        content_by_slide = {
            "Introduction to Machine Learning": """
# Introduction to Machine Learning

## What is Machine Learning?

Machine Learning is a subset of Artificial Intelligence that enables systems to learn and improve from experience without being explicitly programmed.

### Key Concepts:
- **Learning from data**: Algorithms identify patterns in data
- **Prediction**: Making informed predictions based on learned patterns
- **Adaptation**: Models improve over time with more data

### Why Learn Machine Learning?
- High demand in job market
- Powers many modern applications
- Foundation for AI and data science
- Enables data-driven decision making

Machine Learning transforms raw data into actionable insights, revolutionizing how we approach complex problems.
            """,
            "Supervised Learning Basics": """
# Supervised Learning Basics

## What is Supervised Learning?

Supervised Learning is a type of machine learning where algorithms learn from labeled training data.

### Key Components:
- **Input features**: Variables used for prediction
- **Target labels**: Desired outputs
- **Training data**: Labeled examples
- **Model**: Algorithm that learns the relationship

### Common Algorithms:
- **Linear Regression**: Predicts continuous values
- **Logistic Regression**: Predicts binary outcomes
- **Decision Trees**: Makes decisions based on feature values
- **Support Vector Machines**: Finds optimal decision boundaries

### Applications:
- Email spam detection
- Image classification
- Sales forecasting
- Medical diagnosis

Supervised learning turns data into powerful predictive models.
            """
        }

        # Default content
        default_content = f"""
# {current_slide}

## Overview

This section covers the fundamentals of {current_slide} in the context of {topic}.

### Key Topics:
- **Conceptual Understanding**: Learn the core principles
- **Practical Applications**: See how concepts apply to real-world scenarios
- **Hands-on Practice**: Work through examples and exercises
- **Best Practices**: Industry standards and proven methodologies

### Learning Objectives:
By the end of this section, you will:
- Understand the basic concepts and terminology
- Identify practical applications in your field
- Apply the principles to solve simple problems
- Recognize opportunities for further learning

This content will be synchronized with the voice recording to enhance your learning experience.
        """

        return content_by_slide.get(current_slide, default_content)

    def display_slide(self):
        current_slide = st.session_state.current_slide
        topic = st.session_state.topic

        st.title(f"📚 {current_slide}")

        # Progress indicator
        progress = 0.8  # Progress through learning journey
        st.progress(progress)
        st.markdown(f"**Learning: {topic}**")

        # Main slide area - full width and height
        st.markdown("---")

        # Slide content container
        with st.container(height=500):
            # Display formatted slide content
            st.markdown(
                f"""
                <div style="
                    background: white;
                    padding: 2rem;
                    border-radius: 10px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                    height: 100%;
                    overflow-y: auto;
                ">
                    {self.slide_content}
                </div>
                """,
                unsafe_allow_html=True
            )

        # Voice controls section
        st.markdown("---")
        self.voice_controls()

        # Question prompt section
        self.question_prompt()

    def voice_controls(self):
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

        with col1:
            if st.button("⏮️", help="Rewind"):
                st.info("Rewinding 10 seconds...")

        with col2:
            if st.button("⏪", help="Backward"):
                st.info("Going back 5 seconds...")

        with col3:
            # Play/Pause button
            if st.button("▶️ Play", type="primary", use_container_width=True):
                st.success("Playing voice recording...")
                # Simulate voice playback
                time.sleep(2)
                st.warning("Voice recording completed!")

        with col4:
            if st.button("⏩", help="Forward"):
                st.info("Skipping forward 5 seconds...")

        with col5:
            if st.button("⏹️", help="Stop"):
                st.warning("Voice recording stopped.")

    def question_prompt(self):
        st.markdown("---")
        st.markdown("💬 **Ask Questions**")

        # Question input
        user_question = st.text_input(
            "What questions do you have about this topic?",
            placeholder="Type your question here...",
            label_visibility="collapsed"
        )

        # Question buttons
        col1, col2, col3 = st.columns([2, 1, 2])

        with col2:
            if st.button("📤 Ask Question", use_container_width=True):
                if user_question.strip():
                    st.success(f"Question: {user_question}")
                    st.info("Your question has been recorded. An AI tutor will respond shortly!")
                else:
                    st.warning("Please enter a question before asking.")

        # Previous/Next navigation
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 1, 2])

        with col1:
            if st.button("← Previous Slide", use_container_width=True):
                st.info("Navigating to previous slide...")

        with col3:
            if st.button("Next Slide →", use_container_width=True, type="primary"):
                st.info("Moving to next slide...")
                # Navigate to quiz results for demo purposes
                st.session_state.current_page = 'quiz_results'
                st.rerun()

def SlideDisplayInterface():
    interface = SlideDisplayInterfaceClass()