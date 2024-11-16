# middleware.py
import threading

# Use threading.local to store request data
local_data = threading.local()


class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        local_data.request = request  # Store the request in thread-local storage
        response = self.get_response(request)
        return response


def get_current_request():
    return getattr(local_data, "request", None)
