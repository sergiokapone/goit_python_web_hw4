import socket
import urllib.parse
import json
from datetime import datetime

HOST = "localhost"
PORT = 3000
JSON_FILE = "storage/data.json"


def send_html_file(filename, status=200):

    with open(filename, "rb") as file:
        content = file.read()

    response = []

    # Add Headers
    response.append(b"HTTP/1.1 " + str(status).encode() + b" OK")
    response.append(b"Content-type: text/html; charset=utf-8")
    response.append(b"")

    # Add HTML page
    response.append(content)

    return b"\r\n".join(response)


def handle_get_request(request):
    if request.startswith("GET / "):
        return send_html_file("index.html")
    elif request.startswith("GET /message "):
        return send_html_file("message.html")
    else:
        return send_html_file("error.html", status=404)


def handle_post_request(request):
    data = request.split("\r\n")[-1]
    data_parse = urllib.parse.unquote_plus(data)
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

    response = []
    response.append(b"HTTP/1.1 302 Found")
    response.append(b"Location: /")
    response.append(b"")
    response.append(b"")

    return b"\r\n".join(response)


def run_server():

    try:
        print(f"Socket server is running on {HOST}:{PORT}")

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # ---------- Призначаємо ip-адресу і порт > 1024 -------------------- #
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)

        # server_socket.create_server((HOST, PORT)) # альтернативний спосіб

        while True:
            client_socket, addr = server_socket.accept()
            request = client_socket.recv(1024).decode("utf-8")
            print(request)

            if request.startswith("POST"):
                response = handle_post_request(request)
            else:
                response = handle_get_request(request)

            client_socket.send(response)
            client_socket.close()
    except KeyboardInterrupt:
        server_socket.close()
        print("Server stoped...")


if __name__ == "__main__":
    run_server()
