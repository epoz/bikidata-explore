FROM ghcr.io/astral-sh/uv:debian-slim

# Copy dependencies
COPY --link .python-version  pyproject.toml  uv.lock /app/

WORKDIR /app
RUN uv sync --frozen --no-cache

# Copy other content
COPY src /app/

# Start the main application
ENTRYPOINT ["uv", "run", "-m", "uvicorn", "bikidatax:app", "--host", "0.0.0.0", "--port", "8000"]
