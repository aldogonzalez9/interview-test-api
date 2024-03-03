from flask import Response


class ExternalApiError(Exception):
    description = "External API Error"
    code = 502

    def get_response(self):
        return Response(str(self), self.code)
