from django.utils.deprecation import MiddlewareMixin


class CsrfMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response['Access-Control-Allow-Headers'] = 'Content-Type'

        return response
