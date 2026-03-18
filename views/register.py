import json
from user import create_user  # changed from database import create_user


def handle_register(handler):
    if handler.command == "POST":
        process_form(handler)
    else:
        send_json(handler, 405, {"error": "Method not allowed"})


def process_form(handler):
    content_length = int(handler.headers["Content-Length"])
    body = handler.rfile.read(content_length).decode("utf-8")

    # Parse the JSON body into a dictionary
    user = json.loads(body)

    # Pass the whole dictionary straight to create_user — it expects a dict
    response = create_user(user)

    # create_user already returns a JSON string, so we just write it back
    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(response.encode("utf-8"))
