from http.server import HTTPServer
from nss_handler import HandleRequests, status
from views import login_user
from views.register import handle_register


class JSONServer(HandleRequests):

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

        return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_POST(self):
        url = self.parse_url(self.path)

        if url["requested_resource"] == "register":
            handle_register(self)
        else:
            self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_OPTIONS(self):
        url = self.parse_url(self.path)

        if url["requested_resource"] == "register":
            handle_register(self)
        else:
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()


def main():
    host = ""
    port = 8088
    print(f"🚀 Server running on port {port}")
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
