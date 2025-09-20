import streamlit as st
import logging
import os

import networkx as nx
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
            unsafe_allow_html=True,
        )

    def create_interactive_graph(self):
        learning_path = st.session_state.learning_path

        # Create HTML tree structure
        html_content = self.create_tree_html(learning_path)

        # Display the tree
        st.components.v1.html(html_content, height=600, scrolling=False)

    def create_tree_html(self, learning_path):
        # Color gradient from green to blue
        def get_color(index, total):
            green_val = int(100 + index * 25)
            blue_val = int(200 + index * 5)
            return f"rgb(125, {175 + index * 15}, {blue_val})"

        # Create safe HTML with proper escaping
        safe_topics = [topic.replace("'", "&apos;").replace('"', "&quot;") for topic in learning_path]

        # CSS styles
        css = """
        <style>
        .tree {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 20px;
            overflow-x: auto;
            min-width: 100%;
        }
        .node {
            display: inline-block;
            padding: 12px 24px;
            margin: 4px;
            border-radius: 25px;
            color: white;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid white;
            min-width: 200px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            white-space: nowrap;
        }
        .node:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        }
        .node-text {
            display: inline;
            word-wrap: normal;
            max-width: none;
        }
        .connector {
            width: 30px;
            height: 2px;
            background: linear-gradient(to right, #ddd, #ccc);
            border-radius: 1px;
            flex-shrink: 0;
        }
        </style>
        """

        # Create horizontal tree structure
        tree_content = ""
        for i, topic in enumerate(safe_topics):
            color = get_color(i, len(learning_path))

            # Add connecting line (except for first item)
            if i > 0:
                tree_content += "<div class='connector'></div>"

            # Add node with proper navigation to slide_display
            tree_content += f"""
            <div class="node" style="background-color: {color}; border-color: {color};"
                 title="Click to start: {topic}"
                 onclick="navigateToSlide('{topic}')">
                <span class="node-text">{topic}</span>
            </div>
            """

            # Add connector line (except for last item)
            if i < len(learning_path) - 1:
                tree_content += "<div class='connector'></div>"

        # Full HTML document with proper script handling
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Learning Path</title>
            {css}
        </head>
        <body>
            <div class="tree">
                {tree_content}
            </div>

            <!-- Streamlit Component Script -->
            <script>
                // Navigation function to slide display
                function navigateToSlide(topic) {{
                    try {{
                        // Update session state for the selected topic
                        window.parent.postMessage({{
                            'type': 'streamlit:setSessionState',
                            'values': {{
                                'current_slide': topic,
                                'current_page': 'slide_display',
                                'topic': window.parent.document.title || 'learning'
                            }}
                        }}, '*');

                        // Trigger page rerun to navigate to slide display
                        setTimeout(function() {{
                            window.parent.postMessage({{
                                'type': 'streamlit:rerun'
                            }}, '*');
                        }}, 100);

                        console.log('Navigating to slide:', topic);
                    }} catch (error) {{
                        console.log('Navigation failed:', error);

                        // Fallback: try to set component value
                        try {{
                            window.parent.postMessage({{
                                'type': 'streamlit:setComponentValue',
                                'value': {{
                                    'type': 'topic_click',
                                    'topic': topic,
                                    'navigate': true
                                }}
                            }}, '*');
                        }} catch (fallbackError) {{
                            console.log('Fallback navigation also failed:', fallbackError);
                        }}
                    }}
                }}

                // Handle component unmount
                window.addEventListener('beforeunload', function() {{
                    // Clean up if needed
                    console.log('Component unmounting');
                }});
            </script>
        </body>
        </html>
        """

        return html

def LearningPathInterface():
    interface = LearningPathInterfaceClass()