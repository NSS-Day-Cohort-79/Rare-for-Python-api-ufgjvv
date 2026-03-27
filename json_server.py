"""JSONServer for Rare Python API

HTTP server with routes for users, posts, categories, and tags.
Handles GET, POST, PUT, DELETE requests.
"""

from http.server import HTTPServer
import json
from views import (
    login_user,
    get_categories,
    get_tags,
    post_post,
    create_category,
    get_user_posts,
    create_user,
    get_posts,
    update_category,
    get_category,
    delete_category,
)
from views.posts import get_single_post  # For Post Details (Ticket #5)
from nss_handler import HandleRequests, status


class JSONServer(HandleRequests):
    """HTTP server for Rare Python API with routes for users, posts, categories, and tags"""

    def do_GET(self):  # noqa: N802
        """Handle GET requests"""
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
            query_params = url["query_params"]
            if "id" in query_params:
                pk = query_params["id"]
                return self.response(get_category(pk[0]), status.HTTP_200_SUCCESS.value)
            return self.response(get_categories(), status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "tags":
            return self.response(get_tags(), status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "posts":
            if url.get("pk") is not None:
                return self.response(
                    get_single_post(url["pk"]), status.HTTP_200_SUCCESS.value
                )
            else:
                query_params = url["query_params"]
                if "user_id" in query_params:
                    return self.response(
                        get_user_posts(query_params["user_id"][0]),
                        status.HTTP_200_SUCCESS.value,
                    )
                else:
                    return self.response(get_posts(None), status.HTTP_200_SUCCESS.value)

        return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_POST(self):  # noqa: N802
        """Handle POST requests"""
        url = self.parse_url(self.path)

        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "register":
            return self.response(
                create_user(request_body), status.HTTP_201_SUCCESS_CREATED.value
            )

        elif url["requested_resource"] == "posts":
            return self.response(
                post_post(request_body), status.HTTP_201_SUCCESS_CREATED.value
            )

        elif url["requested_resource"] == "categories":
            if not request_body.get("label", "").strip():
                return self.response(
                    json.dumps({"message": "Category label is required."}),
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )
            return self.response(
                create_category(request_body), status.HTTP_201_SUCCESS_CREATED.value
            )

        return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_PUT(self):  # noqa: N802
        """Handle PUT requests"""
        url = self.parse_url(self.path)

        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "categories":
            if not request_body.get("label", "").strip():
                return self.response(
                    json.dumps({"message": "Category label is required."}),
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )
            return self.response(
                update_category(request_body), status.HTTP_200_SUCCESS.value
            )

        return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_DELETE(self):  # noqa: N802
        """Handle DELETE requests"""
        url = self.parse_url(self.path)
        pk = url.get("pk")

        if url["requested_resource"] == "categories" and pk is not None:
            successfully_deleted = delete_category(pk)
            if successfully_deleted:
                return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

        return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)


def main():
    """Start the JSONServer on localhost:8088"""
    host = "127.0.0.1"
    port = 8088
    print(f"🚀 Server running on {host}:{port}")
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
