import json
import socket
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import threading
import logging

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)


HOST = "0.0.0.0"
HTTP_PORT = 3000
SOCKET_PORT = 5000
JSON_FILE = "c:/storage/data.json"


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/message":
            self.send_html_file("message.html")
        else:
            self.send_html_file("error.html", 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {
            key: value for key, value in [el.split("=") for el in data_parse.split("&")]
        }
        timestamp = datetime.now().isoformat()

        new_data = {timestamp: data_dict}

        with open(JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        data.update(new_data)

        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)

        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()


def run_HTTP_server():
    logger.info(f"HTTP server is running on port {HTTP_PORT}")
    server_address = (HOST, HTTP_PORT)
    http = HTTPServer(server_address, HttpHandler)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def run_Socket_server():
    logger.info(f"UDP socket server is running on port {SOCKET_PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, SOCKET_PORT))

        while True:
            data, address = sock.recvfrom(1024)
            json_data = data.decode("utf-8")

            message = json.loads(json_data)

            save_message_to_json(message)


def save_message_to_json(message):
    timestamp = message.get("timestamp")
    username = message.get("username")
    text = message.get("message")

    if timestamp and username and text:
        with open(JSON_FILE, "a") as file:
            data = {"username": username, "message": text}
            json.dump(data, file)
            file.write("\n")


if __name__ == "__main__":
    threads = []
    # Створення та запуск потоку для HTTP-сервера
    http_thread = threading.Thread(target=run_HTTP_server)
    http_thread.start()
    threads.append(http_thread)

    # Створення та запуск потоку для сервера сокетов
    socket_thread = threading.Thread(target=run_Socket_server)
    socket_thread.start()
    threads.append(socket_thread)

    # Очкування завершення роботи потоків
    for thread in threads:
        thread.join()
