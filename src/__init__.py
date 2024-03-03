import logging
import os
from src.config.config import Config
from dotenv import load_dotenv
import utils
import log
from flask import Flask, g, json

from src.routes import api
from src.services.exceptions import ExternalApiError

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


@app.errorhandler(ExternalApiError)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps(
        {
            "code": e.code,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


@app.after_request
def apply_caching(response):
    response.headers["X-Trace-Id"] = g.request_id
    return response
