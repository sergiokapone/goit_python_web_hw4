# Домашнє завдання #4

Код виконує дві функції сервера: HTTP-сервера і сервера сокетів.

HTTP-сервер слухає на порту `3000` і обробляє HTTP-запити. Він має два методи: `GET` і `POST`.

Сервер сокетів слухає на порту `5000` і отримує `UDP`-пакети. Він декодує `JSON`-дані з пакету, записує їх у `JSON`-файл і зберігає.

Головна частина коду запускає обидва сервери у власних потоках і очікує їх завершення.

## Docherhub

Образ доступний на [Dockerhub](https://hub.docker.com/repository/docker/sergiokapone/socket_server/general).

Для запуску використовуйте команду

`docker run -p 3000:3000 -p 5000:5000 -v c:/storage:/app/storage sergiokapone/socket_server`

## Локальний запуск

Для безпосереднього запуску `main.py` треба в консолі викликати команду `python main.py`.
