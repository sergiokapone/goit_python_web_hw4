:: Сборка Docker-образа
docker build -t sergiokapone/socket_server .

:: Запуск контейнера с монтированием volumes
docker run -p 3000:3000 -p 5000:5000 -v c:/storage:/app/storage sergiokapone/socket_server
