from flask import json, Response

ERROR_TRACE = "error_trace"


class BaseAPIException(Exception):
    """Base class for API-related exceptions."""

    def get_response(self):
        raise NotImplementedError


def handle_exception(e):
    if issubclass(type(e), BaseAPIException):
        response = e.get_response()
        response_data = {
            "code": e.code,
            "description": e.description,
        }
        if hasattr(e, ERROR_TRACE):
            response_data[ERROR_TRACE] = e.error_trace
        response.data = json.dumps(response_data)
        response.content_type = "application/json"
    else:
        response = Response(
            response=json.dumps({ERROR_TRACE: str(e)}),
            status=500,
            mimetype="application/json",
        )
    return response
