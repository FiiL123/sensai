# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Development
```bash
# Install dependencies and run development server
uv sync
uv run streamlit run app.py

# Run with specific port
uv run streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

### Docker
```bash
# Build and run with Docker Compose
docker-compose up

# Build Docker image
docker build -t sensai .

# Run Docker container
docker run -p 8501:8501 --env-file .env sensai
```

### Environment Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies with uv
uv sync
```

## Architecture

### Application Flow
This is a Streamlit-based LLM learning application that follows a multi-step learning journey:

1. **Topic Selection** (`src/components/topic_selection.py`) - User enters desired topic to learn
2. **Quiz Interface** (`src/components/quiz.py`) - Dynamic question generation using z.ai to assess knowledge level
3. **Learning Path** (`src/components/learning_path.py`) - NetworkX-based interactive graph showing personalized learning path
4. **Slide Display** (`src/components/slide_display.py`) - Interactive learning slides with voice controls
5. **Quiz Results** (`src/components/quiz_results.py`) - Final assessment with AI evaluation

### Key Dependencies
- **Streamlit**: Frontend framework for the interactive web interface
- **zai-sdk**: LLM integration for dynamic question generation (glm-4.5 model)
- **networkx**: Graph construction for learning path visualization
- **plotly**: Interactive graph visualization in the learning path component
- **elevenlabs**: Text-to-speech for voice explanations
- **python-dotenv**: Environment variable management

### Environment Configuration
The application requires several API configurations in `.env`:
- `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN` for z.ai integration
- Google Cloud Text-to-Speech configuration with service account credentials
- Various audio generation and caching settings

### Session State Management
The application uses Streamlit session state extensively to track:
- Current page in the learning journey
- User's selected topic
- Quiz answers and questions
- Learning path nodes
- Current slide content
- Quiz results

### Component Architecture
Each component is a self-contained class with its own interface methods:
- All components inherit from Streamlit and use st.session_state for state management
- The main app (`app.py`) handles routing between components based on session state
- Components are modular and can be developed independently

### Error Handling
- Graceful fallback to hardcoded questions if z.ai API fails
- Basic validation for user inputs and API responses
- Logging for debugging API integration issues

### Testing
No formal test framework is currently configured. Development should focus on manual testing through the Streamlit interface.