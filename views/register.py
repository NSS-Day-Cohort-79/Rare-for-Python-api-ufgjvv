import json
from .user import create_user


def handle_register(handler):
    if handler.command == "POST":
        process_form(handler)
    elif handler.command == "OPTIONS":
        handle_options(handler)
    else:
        send_json(handler, 405, {"error": "Method not allowed"})


def process_form(handler):
    try:
        content_length = int(handler.headers["Content-Length"])
        body = handler.rfile.read(content_length).decode("utf-8")
        user = json.loads(body)
    except (ValueError, KeyError, json.JSONDecodeError, UnicodeDecodeError):
        send_json(handler, 400, {"error": "Invalid JSON"})
        return

    response = create_user(user)
    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(response.encode("utf-8"))


def handle_options(handler):
    handler.send_response(200)
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.end_headers()


def send_json(handler, status, data):
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(json.dumps(data).encode("utf-8"))
