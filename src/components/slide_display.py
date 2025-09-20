import streamlit as st
import time
import json

class SlideDisplayInterfaceClass:
    def __init__(self):
        # Initialize session state for voice playback
        if 'voice_playing' not in st.session_state:
            st.session_state.voice_playing = False
        if 'voice_progress' not in st.session_state:
            st.session_state.voice_progress = 0

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

        # Hide Streamlit default elements and create full-page slide layout
        st.markdown(
            """
            <style>
            /* Hide default Streamlit elements */
            div[data-testid="stHeader"], div[data-testid="stSidebar"], .main .block-container {
                display: none !important;
            }

            /* Full page layout with no scrollbars */
            html, body, .stApp, .main {
                margin: 0 !important;
                padding: 0 !important;
                overflow: hidden !important;
                height: 100vh !important;
                width: 100vw !important;
            }

            /* Slide container */
            .slide-container {
                width: 100vw;
                height: 100vh;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                flex-direction: column;
                position: fixed;
                top: 0;
                left: 0;
            }

            /* Main slide content */
            .slide-main {
                width: 100%;
                height: 100vh;
                background: white;
                display: flex;
                flex-direction: column;
            }

            /* Slide header */
            .slide-header {
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
                color: white;
                padding: 2rem 3rem;
                border-radius: 0;
            }

            .slide-title {
                font-size: 2.5rem;
                font-weight: 700;
                margin: 0;
                line-height: 1.2;
            }

            .slide-subtitle {
                font-size: 1.2rem;
                opacity: 0.9;
                margin: 0.5rem 0 0 0;
                font-weight: 400;
            }

            /* Slide body - scrollable content area */
            .slide-body {
                flex: 1;
                padding: 2.5rem 3rem;
                overflow-y: auto;
                max-height: calc(100vh - 200px); /* Leave space for control panel */
            }

            /* Floating control panel */
            .control-panel {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                border-top: 1px solid rgba(255, 255, 255, 0.2);
                padding: 1rem 2rem;
                box-shadow: 0 -10px 30px rgba(0,0,0,0.1);
                z-index: 1000;
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 1rem;
                height: auto;
            }

            /* Control panel sections */
            .control-section {
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }

            .control-btn {
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
                color: white;
                border: none;
                border-radius: 8px;
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                font-size: 1.2rem;
                transition: all 0.3s ease;
            }

            .control-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
            }

            .play-pause.playing {
                background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            }

            /* Progress bar */
            .progress-container {
                width: 150px;
                height: 6px;
                background: #e5e7eb;
                border-radius: 3px;
                overflow: hidden;
            }

            .progress-bar {
                height: 100%;
                background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
                border-radius: 3px;
                transition: width 0.3s ease;
            }

            /* Question input */
            .question-input {
                padding: 0.5rem 1rem;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                font-size: 0.9rem;
                width: 250px;
                outline: none;
                transition: border-color 0.3s ease;
            }

            .question-input:focus {
                border-color: #4f46e5;
            }

            /* Ask button */
            .ask-btn {
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                cursor: pointer;
                font-size: 0.9rem;
                transition: all 0.3s ease;
            }

            .ask-btn:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
            }

            /* Navigation buttons */
            .nav-btn {
                background: #f3f4f6;
                color: #374151;
                border: none;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                cursor: pointer;
                font-size: 0.9rem;
                transition: all 0.3s ease;
            }

            .nav-btn:hover {
                background: #e5e7eb;
            }

            .nav-btn.primary {
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
                color: white;
            }

            .nav-btn.primary:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Create full-page slide using HTML rendering
        st.markdown("""
        <div class="slide-container">
            <div class="slide-main">
                <div class="slide-header">
                    <h1 class="slide-title">{}</h1>
                    <p class="slide-subtitle">Learning Module: {}</p>
                </div>
                <div class="slide-body">
        """.format(current_slide, topic), unsafe_allow_html=True)

        # Display slide content
        self._format_slide_content()

        # Close slide body and main container
        st.markdown("""
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Add control panel
        play_pause_text = "⏸️" if st.session_state.voice_playing else "▶️"
        play_pause_class = "play-pause playing" if st.session_state.voice_playing else ""

        control_panel_html = f"""
        <div class="control-panel">
            <div class="control-section">
                <button class="control-btn" onclick="function() {{ alert('Rewind 10 seconds'); }}" title="Rewind 10 seconds">⏮️</button>
                <button class="control-btn" onclick="function() {{ alert('Backward 5 seconds'); }}" title="Backward 5 seconds">⏪</button>
                <button class="control-btn {play_pause_class}" onclick="function() {{ alert('Toggle voice'); }}" title="Play/Pause">{play_pause_text}</button>
                <button class="control-btn" onclick="function() {{ alert('Forward 5 seconds'); }}" title="Forward 5 seconds">⏩</button>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {st.session_state.voice_progress}%"></div>
                </div>
            </div>
            <div class="control-section">
                <input type="text" class="question-input" placeholder="Type your question here..." id="question_input">
                <button class="ask-btn" onclick="function() {{
                    const question = document.getElementById('question_input').value;
                    if(question) alert('Question: ' + question);
                }}">📤 Ask</button>
            </div>
            <div class="control-section">
                <button class="nav-btn" onclick="function() {{ alert('Previous slide'); }}" title="Previous slide">← Previous Slide</button>
                <button class="nav-btn primary" onclick="function() {{ alert('Next slide'); }}" title="Next slide">Next Slide →</button>
            </div>
        </div>
        """

        st.markdown(control_panel_html, unsafe_allow_html=True)


    def _render_slide_content(self, current_slide, topic):
        """Render PowerPoint-style slide content"""
        return self._format_slide_content()

    def _format_slide_content(self):
        """Format slide content with proper PowerPoint styling using Streamlit components"""
        content = self.slide_content

        # Split content into lines and process them
        lines = content.split('\n')
        bullet_points = []

        for line in lines:
            stripped_line = line.strip()

            if not stripped_line:
                # Empty line, add spacing
                st.markdown("<br><br>", unsafe_allow_html=True)
                continue

            # Collect bullet points first
            if stripped_line.startswith("-"):
                bullet_text = stripped_line[1:].strip()
                bullet_points.append(bullet_text)
                continue

            # Handle headers using Streamlit's built-in components
            if stripped_line.startswith("# "):
                st.title(stripped_line[2:])
            elif stripped_line.startswith("## "):
                st.header(stripped_line[3:])
            elif stripped_line.startswith("### "):
                st.subheader(stripped_line[4:])
            elif stripped_line.startswith("**") and stripped_line.endswith("**") and "**" in stripped_line[1:-1]:
                # Handle bold text
                bold_text = stripped_line[2:-2]
                st.markdown(f"**{bold_text}**")
            else:
                # Handle regular paragraphs
                if stripped_line:
                    st.markdown(f"#### {stripped_line}" if not stripped_line.startswith(("## ", "### ", "# ")) else stripped_line)

        # Render bullet points in a nice container
        if bullet_points:
            st.markdown("""
            <div style="background: #f8fafc; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
            <h4 style="margin: 0 0 1rem 0; color: #1f2937;">Key Topics:</h4>
            <ul style="margin: 0; padding-left: 1.5rem;">
            """, unsafe_allow_html=True)

            for point in bullet_points:
                st.markdown(f"<li style='margin: 0.5rem 0; color: #4b5563;'>{point}</li>", unsafe_allow_html=True)

            st.markdown("</ul></div>", unsafe_allow_html=True)

    def _render_control_panel(self):
        """Render control panel using HTML structure"""
        play_pause_text = "⏸️" if st.session_state.voice_playing else "▶️"
        play_pause_class = "play-pause playing" if st.session_state.voice_playing else ""

        return f"""
        <div class="control-section">
            <button class="control-btn" onclick="function() {{ alert('Rewind 10 seconds'); }}" title="Rewind 10 seconds">⏮️</button>
            <button class="control-btn" onclick="function() {{ alert('Backward 5 seconds'); }}" title="Backward 5 seconds">⏪</button>
            <button class="control-btn {play_pause_class}" onclick="function() {{ alert('Toggle voice'); }}" title="Play/Pause">{play_pause_text}</button>
            <button class="control-btn" onclick="function() {{ alert('Forward 5 seconds'); }}" title="Forward 5 seconds">⏩</button>
            <div class="progress-container">
                <div class="progress-bar" style="width: {st.session_state.voice_progress}%"></div>
            </div>
        </div>
        <div class="control-section">
            <input type="text" class="question-input" placeholder="Type your question here..." id="question_input">
            <button class="ask-btn" onclick="function() {{
                const question = document.getElementById('question_input').value;
                if(question) alert('Question: ' + question);
            }}">📤 Ask</button>
        </div>
        <div class="control-section">
            <button class="nav-btn" onclick="function() {{ alert('Previous slide'); }}" title="Previous slide">← Previous Slide</button>
            <button class="nav-btn primary" onclick="function() {{ alert('Next slide'); }}" title="Next slide">Next Slide →</button>
        </div>
        """

    def toggle_voice(self):
        """Toggle voice playback"""
        st.session_state.voice_playing = not st.session_state.voice_playing
        if st.session_state.voice_playing:
            st.success("Voice recording started...")
        else:
            st.warning("Voice recording paused.")

    def rewind_audio(self):
        """Rewind audio by 10 seconds"""
        st.session_state.voice_progress = max(0, st.session_state.voice_progress - 10)
        st.info("Rewinding 10 seconds...")

    def backward_audio(self):
        """Backward audio by 5 seconds"""
        st.session_state.voice_progress = max(0, st.session_state.voice_progress - 5)
        st.info("Going back 5 seconds...")

    def forward_audio(self):
        """Forward audio by 5 seconds"""
        st.session_state.voice_progress = min(100, st.session_state.voice_progress + 5)
        st.info("Skipping forward 5 seconds...")

    def ask_question(self, question):
        """Handle user questions"""
        if question:
            st.success(f"Question submitted: {question}")
            st.info("Your question has been recorded. An AI tutor will respond shortly!")

    def previous_slide(self):
        """Navigate to previous slide"""
        st.info("Navigating to previous slide...")
        # Add actual slide navigation logic here
        # For now, just stay on current slide

    def next_slide(self):
        """Navigate to next slide"""
        st.info("Moving to next slide...")
        # Navigate to quiz results for demo purposes
        st.session_state.current_page = 'quiz_results'
        st.rerun()

    def add_voice_control_handlers(self):
        """No longer needed - using Streamlit native callbacks"""
        pass

def SlideDisplayInterface():
    interface = SlideDisplayInterfaceClass()
    interface.add_voice_control_handlers()