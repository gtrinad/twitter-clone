# Используем базовый образ Python
FROM python:3.11

WORKDIR /app

# Установим зависимости
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем все файлы из текущей директории в образ
COPY app_fast ./app_fast
COPY test ./test
COPY pytest.ini .

# Определяем переменную окружения для PostgreSQL
ENV DATABASE_URL=postgresql+asyncpg://admin:admin@postgres:5432/twitter_db

# Запускаем pytest
CMD ["pytest", "-v", "-s"]
