FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set working directory
WORKDIR /app

# Set environment variables from devcontainer.json
ENV UV_LINK_MODE=symlink

# Copy dependency files first to leverage Docker cache
COPY pyproject.toml uv.lock ./

# Install dependencies (without installing the project itself yet)
RUN uv sync --frozen --no-install-project

# Copy the rest of the application
COPY . /app

# Sync the locked dependencies (the project itself is not a package — deps only).
# 'notebook' is added separately to support the Jupyter entrypoint.
RUN uv sync --frozen --no-install-project && uv pip install notebook

# Add the virtual environment to the PATH
ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["jupyter", "notebook"]
CMD ["--NotebookApp.token=''", "--allow-root", "--ip=0.0.0.0", "--port=8888", "/app"]