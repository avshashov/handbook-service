FROM python:3.12-slim as builder

# --- Install Poetry ---
ARG POETRY_VERSION=1.8.2

ENV POETRY_HOME=/opt/poetry \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_CACHE_DIR=/opt/.cache

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

WORKDIR /handbook-service

# --- Reproduce the environment ---
# You can comment the following two lines if you prefer to manually install
#   the dependencies from inside the container.
COPY pyproject.toml .

# Install the dependencies and clear the cache afterwards.
#   This may save some MBs.
RUN poetry install --no-root --without dev && rm -rf $POETRY_CACHE_DIR

# Copy Application
COPY . /handbook-service

# Now let's build the runtime image from the builder.
#   We'll just copy the env and the PATH reference.
FROM python:3.12-slim as runtime

ENV VIRTUAL_ENV=/handbook-service/.venv
ENV PATH="/handbook-service/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=builder /handbook-service /handbook-service

WORKDIR /handbook-service

# Run Application
RUN chmod +x ./start.sh
CMD ["./start.sh"]
