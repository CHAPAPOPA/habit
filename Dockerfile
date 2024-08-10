FROM python:3.12-slim

# Установите зависимости
RUN apt-get update && apt-get install -y curl gcc libpq-dev

# Установите Poetry
RUN curl -sSL https://install.python-poetry.org | python
ENV POETRY_VERSION=1.8.2 PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.create false
RUN poetry config virtualenvs.in-project true

# Скопируйте файлы pyproject.toml и poetry.lock и установите зависимости
COPY pyproject.toml poetry.lock* /app/
WORKDIR /app
RUN poetry install --no-root

# Скопируйте все файлы проекта
COPY . .