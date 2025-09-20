import streamlit as st

def TopicSelectionInterface():
    st.title("🧠 sensAI - LLM Learning Tool")

    # Center the content
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        # Large header text
        st.markdown(
            """
            <div style="
                font-size: 4rem;
                font-weight: bold;
                text-align: center;
                margin-bottom: 2rem;
                background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">
                I want to learn...
            </div>
            """,
            unsafe_allow_html=True
        )

        # Topic input field
        topic = st.text_input(
            "What topic would you like to study?",
            placeholder="e.g., Machine Learning, Python Programming, Quantum Physics...",
            label_visibility="collapsed",
            key="topic_input"
        )

        # Start Learning button
        if st.button(
            "🚀 Start Learning",
            type="primary",
            use_container_width=True
        ):
            if topic.strip():
                st.session_state.topic = topic.strip()
                st.session_state.current_page = 'quiz'
                st.rerun()
            else:
                st.error("Please enter a topic to learn about.")

        # Instructions
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; color: #666; margin-top: 2rem;">
                <p style="font-size: 1.1rem;">🎯 sensAI will quiz you to understand your current knowledge level</p>
                <p style="font-size: 1.1rem;">📊 Create a personalized learning path based on your needs</p>
                <p style="font-size: 1.1rem;">🎬 Generate interactive slides with voice explanations</p>
                <p style="font-size: 1.1rem;">📝 Test your understanding with a final quiz</p>
            </div>
            """,
            unsafe_allow_html=True
        )