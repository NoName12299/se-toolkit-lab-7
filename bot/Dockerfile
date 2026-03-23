# Используем официальный Python образ
FROM harbor.pg.innopolis.university/docker-hub-cache/python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY bot/pyproject.toml /app/bot/

# Устанавливаем зависимости через pip (конвертируем pyproject.toml в requirements)
RUN pip install --upgrade pip && \
    cd /app/bot && \
    pip install python-telegram-bot httpx pydantic-settings python-dotenv

# Копируем весь код бота
COPY bot/ /app/bot/

# Устанавливаем рабочую директорию в bot
WORKDIR /app/bot

# Создаем non-root пользователя
RUN adduser --disabled-password --gecos "" botuser && \
    chown -R botuser:botuser /app
USER botuser

# Команда запуска
CMD ["python", "bot.py"]
