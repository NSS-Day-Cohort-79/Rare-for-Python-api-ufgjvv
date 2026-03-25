from http.server import HTTPServer
from nss_handler import HandleRequests, status
import json
from views import (
    login_user,
    get_categories,
    get_tags,
    create_tag,
    post_post,
    create_category,
    create_user,
)
from views.register import handle_register


def read_body(handler):
    """Safely read and parse the JSON request body."""
    content_len = int(
        handler.headers.get("Content-Length")
        or handler.headers.get("content-length")
        or 0
    )
    if content_len == 0:
        return {}
    raw = handler.rfile.read(content_len)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


class JSONServer(HandleRequests):

    def do_GET(self):
        url = self.parse_url(self.path)

        if url["requested_resource"] == "users":
            query_params = url["query_params"]
            if "username" in query_params and "password" in query_params:
                credentials = {
                    "username": query_params["username"][0],
                    "password": query_params["password"][0],
                }
                response_body = login_user(credentials)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "categories":
            response_body = json.dumps(get_categories())
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "tags":
            response_body = json.dumps(get_tags())
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "posts":
            return self.response(json.dumps([]), status.HTTP_200_SUCCESS.value)

        return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_POST(self):
        url = self.parse_url(self.path)
        request_body = read_body(self)

        print(f"DEBUG POST resource: {url['requested_resource']}")
        print(f"DEBUG POST body: {request_body}")

        if url["requested_resource"] == "register":
            response_body = create_user(request_body)
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)

        elif url["requested_resource"] == "posts":
            response_body = post_post(request_body)
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)

        elif url["requested_resource"] == "categories":
            if not request_body.get("name", "").strip():
                return self.response(
                    json.dumps({"message": "Category name is required."}),
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )
            response_body = json.dumps(create_category(request_body))
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)

        elif url["requested_resource"] == "tags":
            if not request_body.get("label", "").strip():
                return self.response(
                    json.dumps({"message": "Tag label is required."}),
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )
            response_body = json.dumps(create_tag(request_body))
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)

        else:
            return self.response(
                "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )


def main():
    host = "127.0.0.1"
    port = 8088
    print(f"🚀 Server running on {host}:{port}")
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
