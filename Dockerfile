FROM python:3.12-slim

WORKDIR /app

# Dependencies
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen

# Application
COPY src/ ./src/

# Network & Runtime
EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]