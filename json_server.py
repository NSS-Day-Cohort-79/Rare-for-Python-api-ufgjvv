from http.server import HTTPServer
from nss_handler import HandleRequests, status
import json
from views import login_user, get_categories, get_tags, post_post, create_category
from views.posts import get_single_post, get_user_posts, get_posts
from views import create_user


class JSONServer(HandleRequests):
    """HTTP server for Rare Python API with routes for users, posts, categories, and tags"""

    def do_GET(self):
        response_body = ""
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
            response_body = get_categories()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "tags":
            response_body = get_tags()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "posts":
            if url.get("pk") is not None:
                response_body = get_single_post(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            else:
                query_params = url["query_params"]
                if "user_id" in query_params:
                    response_body = get_user_posts(url, query_params["user_id"][0])
                    return self.response(response_body, status.HTTP_200_SUCCESS.value)
                else:
                    response_body = get_posts(url)
                    return self.response(response_body, status.HTTP_200_SUCCESS.value)

        return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_POST(self):
        url = self.parse_url(self.path)

        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

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
            self.response(
                create_category(request_body), status.HTTP_201_SUCCESS_CREATED.value
            )
        else:
            self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)


def main():
    host = "127.0.0.1"
    port = 8088
    print(f"🚀 Server running on {host}:{port}")
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
