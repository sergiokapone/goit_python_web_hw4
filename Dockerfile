# Указываем базовый образ
FROM python:3.10-alpine

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все файлы проекта в рабочую директорию контейнера
COPY . /app

RUN mkdir -p storage && touch storage/data.json

# Запускаем HTTP-сервер и сервер сокетов
CMD ["python", "main.py"]
