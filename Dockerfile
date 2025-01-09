FROM python:3.12-slim-bullseye

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VERSION=2.0.0
ENV PATH="/opt/poetry/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.create false \
    && poetry install --with main,build --without dev --no-interaction --no-root

RUN mkdir -p dist/system-monitor-app && \
    poetry run pyinstaller build.spec --clean && \
    mv dist/system-monitor dist/system-monitor-app/ && \
    mkdir -p dist/system-monitor-app/data && \
    mkdir -p dist/system-monitor-app/logs && \
    cd dist && \
    tar -czf system-monitor.tar.gz system-monitor-app/

CMD ["cp", "-r", "dist/system-monitor.tar.gz", "/output/"]