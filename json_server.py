import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status

# import sql handling functions from views

# Add your imports below this line
from views import login_user

# GET, PUT, DELETE, POST functions to send data values and requests to sql
class JSONServer(HandleRequests):

    def do_GET(self):
        """Handle GET requests from a client"""

        response_body = ""
        url = self.parse_url(self.path)
        
        if url["requested_resource"] == "users":
            print(url)
            query_params = url["query_params"]
            if "username" in query_params and "password" in query_params:
                username = query_params["username"][0]
                password = query_params["password"][0]
                credentials = {
                    "username": username,
                    "password": password
                }
                response_body = login_user(credentials)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

        else:
            return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
        



def main():
    host = ''
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()

if __name__ == "__main__":
    main()