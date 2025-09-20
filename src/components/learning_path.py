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

        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(learning_path[node])
            # Color gradient from green to blue
            node_colors.append(f"rgb({int(100 + node * 25)}, {int(150 + node * 15)}, {int(200 + node * 5)})")

        # Create Plotly figure
        fig = go.Figure()

        # Add edges
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            mode='lines',
            line=dict(width=2, color='lightgray'),
            hoverinfo='none'
        ))

        # Add nodes
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="bottom center",
            textfont=dict(size=10, family="Arial"),
            marker=dict(
                size=25,
                color=node_colors,
                line=dict(width=2, color='white')
            ),
            hoverinfo='text',
            hovertext=[f"Click to start: {topic}" for topic in learning_path]
        ))

        # Update layout
        fig.update_layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=50, l=50, r=50, t=50),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='white',
            height=600
        )

  # Display the chart
        chart_placeholder = st.plotly_chart(fig, use_container_width=True, key="learning_path_graph")

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