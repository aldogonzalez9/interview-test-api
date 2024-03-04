from flask import Response
from src.error_handlers import BaseAPIException


class ExternalApiError(BaseAPIException):
    description = "External API Error"
    code = 502

    def get_response(self):
        return Response(str(self), self.code)
