"""
json_server.py
--------------
A minimal Python HTTP server that routes REST requests for /tags (and other
resources) to SQL-backed view functions.

Run:
    python json_server.py

Then visit http://localhost:8088/tags
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re

# SQL-backed view functions
from views.tags import get_tags, get_tag, create_tag, update_tag, delete_tag

# ---------------------------------------------------------------------------
# Helper: send a JSON response
# ---------------------------------------------------------------------------

def _json_response(handler, status: int, data):
    """Serialize `data` to JSON and write a complete HTTP response."""
    body = json.dumps(data).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    # Allow cross-origin requests from the React dev server
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.end_headers()
    handler.wfile.write(body)


def _read_body(handler) -> dict:
    """Read and parse the JSON request body. Returns {} on empty/invalid body."""
    length = int(handler.headers.get("Content-Length", 0))
    if length == 0:
        return {}
    raw = handler.rfile.read(length)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


# ---------------------------------------------------------------------------
# Request handler
# ---------------------------------------------------------------------------

class HandleRequests(BaseHTTPRequestHandler):

    # -- CORS pre-flight -------------------------------------------------

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # -- GET -------------------------------------------------------------

    def do_GET(self):
        path = self.path.rstrip("/")

        # GET /tags  → list all tags
        if path == "/tags":
            tags = get_tags()
            _json_response(self, 200, tags)
            return

        # GET /tags/{id}  → single tag
        m = re.fullmatch(r"/tags/(\d+)", path)
        if m:
            tag = get_tag(int(m.group(1)))
            if tag is None:
                _json_response(self, 404, {"error": "Tag not found"})
            else:
                _json_response(self, 200, tag)
            return

        # 404 for unknown routes
        _json_response(self, 404, {"error": f"Route '{self.path}' not found"})

    # -- POST ------------------------------------------------------------

    def do_POST(self):
        path = self.path.rstrip("/")

        # POST /tags  → create a new tag
        if path == "/tags":
            body = _read_body(self)
            try:
                new_tag = create_tag(body)
                _json_response(self, 201, new_tag)
            except ValueError as exc:
                _json_response(self, 400, {"error": str(exc)})
            return

        _json_response(self, 404, {"error": f"Route '{self.path}' not found"})

    # -- PUT -------------------------------------------------------------

    def do_PUT(self):
        path = self.path.rstrip("/")

        # PUT /tags/{id}  → update an existing tag
        m = re.fullmatch(r"/tags/(\d+)", path)
        if m:
            body = _read_body(self)
            try:
                updated = update_tag(int(m.group(1)), body)
                if updated is None:
                    _json_response(self, 404, {"error": "Tag not found"})
                else:
                    _json_response(self, 200, updated)
            except ValueError as exc:
                _json_response(self, 400, {"error": str(exc)})
            return

        _json_response(self, 404, {"error": f"Route '{self.path}' not found"})

    # -- DELETE ----------------------------------------------------------

    def do_DELETE(self):
        path = self.path.rstrip("/")

        # DELETE /tags/{id}
        m = re.fullmatch(r"/tags/(\d+)", path)
        if m:
            deleted = delete_tag(int(m.group(1)))
            if deleted:
                _json_response(self, 200, {"deleted": True})
            else:
                _json_response(self, 404, {"error": "Tag not found"})
            return

        _json_response(self, 404, {"error": f"Route '{self.path}' not found"})

    # -- Suppress default request logs (optional) ------------------------

    def log_message(self, fmt, *args):
        print(f"[{self.address_string()}] {fmt % args}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    HOST, PORT = "localhost", 8088
    server = HTTPServer((HOST, PORT), HandleRequests)
    print(f"Server running at http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")