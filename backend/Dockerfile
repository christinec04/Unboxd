FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files first
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen

# Copy the rest of the app
COPY . .

EXPOSE 8000

CMD ["uv", "run", "main.py"]