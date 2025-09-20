import streamlit as st
from src.components.topic_selection import TopicSelectionInterface
from src.components.quiz import QuizInterface
from src.components.learning_path import LearningPathInterface
from src.components.slide_display import SlideDisplayInterface
from src.components.quiz_results import QuizResultsInterface

def main():
    st.set_page_config(
        page_title="sensAI - LLM Learning Tool",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'topic_selection'
        st.session_state.topic = ''
        st.session_state.quiz_answers = []
        st.session_state.learning_path = []
        st.session_state.current_slide = None
        st.session_state.quiz_results = {}

    # Hide the default Streamlit menu and footer
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Navigation
    if st.session_state.current_page == 'topic_selection':
        TopicSelectionInterface()
    elif st.session_state.current_page == 'quiz':
        QuizInterface()
    elif st.session_state.current_page == 'learning_path':
        LearningPathInterface()
    elif st.session_state.current_page == 'slide_display':
        SlideDisplayInterface()
    elif st.session_state.current_page == 'quiz_results':
        QuizResultsInterface()

if __name__ == "__main__":
    main()