FROM python:3.12-slim

# Set working directory
WORKDIR /app
run pip install uv
# Copy requirements file and install dependencies
COPY pyproject.toml .
RUN uv sync

# Copy source code
COPY src/ ./src/
COPY app.py .

# Expose port
EXPOSE 8501

# Run the Streamlit app
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]