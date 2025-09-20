import logging
import os

import networkx as nx
import plotly.graph_objects as go
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

        # Create a linear graph structure
        G = nx.Graph()

        # Add nodes
        for i, topic in enumerate(learning_path):
            G.add_node(i, label=topic)

        # Add edges (sequential connections)
        for i in range(len(learning_path) - 1):
            G.add_edge(i, i + 1)

        # Create layout
        pos = nx.spring_layout(G, k=3, iterations=50)

        # Create edge trace
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        node_sizes = []

        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(learning_path[node])
            # Color progression from green (easy) to purple (advanced)
            progress = node / (len(learning_path) - 1) if len(learning_path) > 1 else 0
            node_colors.append(
                f"rgb({int(50 + progress * 150)}, {int(200 - progress * 100)}, {int(100 + progress * 155)})"
            )
            # Size nodes based on position
            node_sizes.append(20 + (len(learning_path) - node) * 2)

        # Create Plotly figure
        fig = go.Figure()

        # Add edges
        fig.add_trace(
            go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(width=3, color="#e0e0e0"), hoverinfo="none")
        )

        # Add nodes
        fig.add_trace(
            go.Scatter(
                x=node_x,
                y=node_y,
                mode="markers+text",
                text=node_text,
                textposition="bottom center",
                textfont=dict(size=10, family="Arial", color="#333"),
                marker=dict(size=node_sizes, color=node_colors, line=dict(width=2, color="white")),
                hoverinfo="text",
                hovertext=[f"📚 Click to start learning: {topic}" for topic in learning_path],
            )
        )

        # Add progress indicators on nodes
        fig.add_trace(
            go.Scatter(
                x=node_x,
                y=node_y,
                mode="text",
                text=[f"Step {i + 1}" for i in range(len(learning_path))],
                textposition="top center",
                textfont=dict(size=8, color="#666", family="Arial"),
                hoverinfo="none",
            )
        )

        # Update layout
        fig.update_layout(
            showlegend=False,
            hovermode="closest",
            margin=dict(b=80, l=50, r=50, t=30),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor="white",
            height=650,
            title_x=0.5,
            title_font=dict(size=16, family="Arial"),
        )

        # Display the chart
        st.plotly_chart(fig, use_container_width=True, key="learning_path_graph")

        # Add clickable buttons for each node below the chart
        st.markdown("---")
        st.markdown("### **Click on a topic to start learning:**")

        # Create columns for the topic buttons
        cols = st.columns(len(learning_path))

        for i, topic in enumerate(learning_path):
            with cols[i]:
                if st.button(topic, key=f"node_{i}", use_container_width=True):
                    st.session_state.current_slide = topic
                    st.session_state.current_page = "slide_display"
                    st.rerun()


def LearningPathInterface():
    interface = LearningPathInterfaceClass()
