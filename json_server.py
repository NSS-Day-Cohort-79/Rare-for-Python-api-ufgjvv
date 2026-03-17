import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status

# import sql handling functions from views

# Add your imports below this line
from views import login_user, create_user

# GET, PUT, DELETE, POST functions to send data values and requests to sql
class JSONServer(HandleRequests):

    def do_GET(self):
        """Handle GET requests from a client"""

        response_body = ""
        url = self.parse_url(self.path)

        # if url["requested_resource"] == "categories":
        #     if url["pk"] != 0:
        #         response_body = retrieve_dock(url["pk"])
        #         return self.response(response_body, status.HTTP_200_SUCCESS.value)

        #     response_body = list_docks()
        #     return self.response(response_body, status.HTTP_200_SUCCESS.value)

        # elif url["requested_resource"] == "comments":
        #     if url["pk"] != 0:
        #         response_body = retrieve_hauler(url["pk"])
        #         return self.response(response_body, status.HTTP_200_SUCCESS.value)

        #     response_body = list_haulers()
        #     return self.response(response_body, status.HTTP_200_SUCCESS.value)

        # elif url["requested_resource"] == "posts":
        #     if url["pk"] != 0:
        #         response_body = retrieve_ship(url["pk"])
        #         return self.response(response_body, status.HTTP_200_SUCCESS.value)

        #     response_body = list_ships(url)
        #     return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
        # elif url["requested_resource"] == "tags":
        #     if url["pk"] != 0:
        #         response_body = retrieve_ship(url["pk"])
        #         return self.response(response_body, status.HTTP_200_SUCCESS.value)

        #     response_body = list_ships(url)
        #     return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
        if url["requested_resource"] == "users":
            if url["pk"] != 0:
                response_body = retrieve_ship(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            
            elif url["username", "password"] != 0:
                response_body = login_user(url["username", "password"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = list_ships(url)
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        else:
            return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    # def do_PUT(self):
    #     """Handle PUT requests from a client"""

    #     # Parse the URL and get the primary key
    #     url = self.parse_url(self.path)
    #     pk = url["pk"]

    #     # Get the request body JSON for the new data
    #     content_len = int(self.headers.get('content-length', 0))
    #     request_body = self.rfile.read(content_len)
    #     request_body = json.loads(request_body)

    #     if url["requested_resource"] == "categories":
    #         if url["pk"] != 0:
    #             response_body = retrieve_dock(url["pk"])
    #             return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #         response_body = list_docks()
    #         return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #     elif url["requested_resource"] == "comments":
    #         if url["pk"] != 0:
    #             response_body = retrieve_hauler(url["pk"])
    #             return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #         response_body = list_haulers()
    #         return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #     elif url["requested_resource"] == "posts":
    #         if url["pk"] != 0:
    #             response_body = retrieve_ship(url["pk"])
    #             return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #         response_body = list_ships(url)
    #         return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
    #     elif url["requested_resource"] == "tags":
    #         if url["pk"] != 0:
    #             response_body = retrieve_ship(url["pk"])
    #             return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #         response_body = list_ships(url)
    #         return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
    #     elif url["requested_resource"] == "users":
    #         if url["pk"] != 0:
    #             response_body = retrieve_ship(url["pk"])
    #             return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #         response_body = list_ships(url)
    #         return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #     else:
    #         return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    # def do_DELETE(self):
    #     """Handle DELETE requests from a client"""

    #     url = self.parse_url(self.path)
    #     pk = url["pk"]

    #     if url["requested_resource"] == "categories":
    #         if url["pk"] != 0:
    #             response_body = retrieve_dock(url["pk"])
    #             return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #         response_body = list_docks()
    #         return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #     elif url["requested_resource"] == "comments":
    #         if url["pk"] != 0:
    #             response_body = retrieve_hauler(url["pk"])
    #             return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #         response_body = list_haulers()
    #         return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #     elif url["requested_resource"] == "posts":
    #         if url["pk"] != 0:
    #             response_body = retrieve_ship(url["pk"])
    #             return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #         response_body = list_ships(url)
    #         return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
    #     elif url["requested_resource"] == "tags":
    #         if url["pk"] != 0:
    #             response_body = retrieve_ship(url["pk"])
    #             return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #         response_body = list_ships(url)
    #         return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
    #     elif url["requested_resource"] == "users":
    #         if url["pk"] != 0:
    #             response_body = retrieve_ship(url["pk"])
    #             return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #         response_body = list_ships(url)
    #         return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #     else:
    #         return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    # def do_POST(self):
    #     """Handle POST requests from a client"""
    #     url = self.parse_url(self.path)

    #     content_len = int(self.headers.get('content-length', 0))
    #     request_body = self.rfile.read(content_len)
    #     request_body = json.loads(request_body)

    #     if url["requested_resource"] == "categories":
    #         if url["pk"] != 0:
    #             response_body = retrieve_dock(url["pk"])
    #             return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #         response_body = list_docks()
    #         return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #     elif url["requested_resource"] == "comments":
    #         if url["pk"] != 0:
    #             response_body = retrieve_hauler(url["pk"])
    #             return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #         response_body = list_haulers()
    #         return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #     elif url["requested_resource"] == "posts":
    #         if url["pk"] != 0:
    #             response_body = retrieve_ship(url["pk"])
    #             return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #         response_body = list_ships(url)
    #         return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
    #     elif url["requested_resource"] == "tags":
    #         if url["pk"] != 0:
    #             response_body = retrieve_ship(url["pk"])
    #             return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #         response_body = list_ships(url)
    #         return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
    #     elif url["requested_resource"] == "users":
    #         if url["pk"] != 0:
    #             response_body = retrieve_ship(url["pk"])
    #             return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #         response_body = list_ships(url)
    #         return self.response(response_body, status.HTTP_200_SUCCESS.value)

    #     else:
    #         return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
        







#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    host = ''
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()

if __name__ == "__main__":
    main()