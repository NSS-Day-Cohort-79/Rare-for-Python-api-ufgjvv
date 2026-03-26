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
)
import json


class JSONServer(nss_handler.HandleRequests):

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
                return self.response(
                    response_body, nss_handler.status.HTTP_200_SUCCESS.value
                )

        elif url["requested_resource"] == "categories":
            print(url)
            query_params = url["query_params"]
            if "id" in query_params:
                pk = query_params["id"]
                response_body = get_category(pk[0])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            response_body = get_categories()
            return self.response(
                response_body, nss_handler.status.HTTP_200_SUCCESS.value
            )

        elif url["requested_resource"] == "tags":
            response_body = get_tags()
            return self.response(
                response_body, nss_handler.status.HTTP_200_SUCCESS.value
            )
            print(url)

        elif url["requested_resource"] == "posts":
            print(url)
            query_params = url["query_params"]
            dict_list = query_params.values()
            list_of_values = list(dict_list)
            if "user_id" in query_params:
                user = list_of_values[0]
                response_body = get_user_posts(url, user[0])
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

        # ✅ REGISTER
        if url["requested_resource"] == "register":
            response_body = create_user(request_body)
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)

        # ✅ POSTS
        elif url["requested_resource"] == "posts":
            response_body = post_post(request_body)
            return self.response(
                response_body, nss_handler.status.HTTP_201_SUCCESS_CREATED.value
            )

        elif url["requested_resource"] == "categories":

            if not request_body.get("label", "").strip():
                return self.response(
                    json.dumps({"message": "Category label is required."}),
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )
            self.response(
                create_category(request_body), status.HTTP_201_SUCCESS_CREATED.value
            )
        else:
            return self.response(
                "", nss_handler.status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )

    def do_PUT(self):
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
            self.response(update_category(request_body), status.HTTP_200_SUCCESS.value)


def main():
    host = "127.0.0.1"
    port = 8088
    print(f"🚀 Server running on {host}:{port}")
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
