import logging
import os
from src.config.config import Config
from dotenv import load_dotenv
import utils
import log
from flask import Flask, g, json, Response

from src.routes import api

ERROR_TRACE = "error_trace"

# loading environment variables
load_dotenv()

# declaring flask application
app = Flask(__name__)
logger = logging.getLogger("__name__")

logger.info("Calling configuration")
config = Config().dev_config

logger.info("Setting environment")
app.env = config.ENV


app.register_blueprint(api, url_prefix="/api")


@app.errorhandler(Exception)
def handle_exception(e):
    if not hasattr(e, "get_response"):
        response = Response(
            response=json.dumps({ERROR_TRACE: str(e)}),
            status=500,
            mimetype="application/json",
        )
    else:
        response = e.get_response()
        response_data = {
            "code": e.code,
            "description": e.description,
        }
        if hasattr(e, ERROR_TRACE):
            response_data[ERROR_TRACE] = e.error_trace
        response.data = json.dumps(response_data)
        response.content_type = "application/json"
    return response


@app.after_request
def apply_headers(response):
    if hasattr(g, "request_id"):
        response.headers["X-Trace-Id"] = g.request_id
    return response
