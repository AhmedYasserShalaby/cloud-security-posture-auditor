FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml requirements.txt ./
COPY src ./src
COPY app ./app
COPY config ./config
COPY docs ./docs
COPY data ./data
RUN pip install --no-cache-dir -e ".[dev]"

EXPOSE 8501
CMD ["streamlit", "run", "app/streamlit_dashboard.py", "--server.address=0.0.0.0", "--server.port=8501"]
