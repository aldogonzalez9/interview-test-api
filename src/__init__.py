import logging
import os
from src.config.config import Config
from dotenv import load_dotenv
import utils
import log
from flask import Flask, g, json, Response
from src.error_handlers import handle_exception

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
app.register_error_handler(Exception, handle_exception)


@app.after_request
def apply_headers(response):
    if hasattr(g, "request_id"):
        response.headers["X-Trace-Id"] = g.request_id
    return response
