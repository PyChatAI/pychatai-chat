# Stage 1: init
FROM python:3.11 as init

# Pass `--build-arg API_URL=http://app.example.com:8000` during build
ARG API_URL

# Copy local context to `/app` inside container (see .dockerignore)
WORKDIR /app
COPY . .

# Create virtualenv which will be copied into final container
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3.11 -m venv $VIRTUAL_ENV

ENV POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

# Install Poetry and packages
RUN curl -sSL https://install.python-poetry.org | python3 -
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --only main


# Deploy templates and prepare app

# Stage 2: copy artifacts into slim image
FROM python:3.11
ARG API_URL
WORKDIR /app
COPY --from=init /app /app
ENV PATH="/app/.venv/bin:$PATH" API_URL=$API_URL
RUN reflex init

CMD reflex db migrate && reflex run --env prod
