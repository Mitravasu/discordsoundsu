# Use Python 3.14 slim image as base
FROM python:3.14-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml ./
COPY .python-version ./
COPY README.md ./
COPY uv.lock ./
COPY .env ./
COPY src ./src

# mp3 folder should be mounted as a volume at runtime
# docker run -v ./mp3:/app/mp3 ...
RUN mkdir -p mp3

# Install dependencies using uv
RUN uv sync --frozen

# Run the Discord bot
CMD ["uv", "run", "discordsoundsu"]
