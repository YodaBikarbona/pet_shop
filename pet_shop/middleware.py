import logging

logger = logging.getLogger(__name__)


class CustomMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_url = request.path_info.split("v1/")[-1]
        request.current_url = current_url
        return self.get_response(request)
