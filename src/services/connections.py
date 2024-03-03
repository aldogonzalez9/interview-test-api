from requests.compat import urljoin
import logging
import requests
import urllib.parse

logger = logging.getLogger("tax_calculator.connections")

GET = "GET"


def build_url(base_url, resource_path, params={}):
    url = urljoin(base=base_url, url=resource_path)
    if params:
        params_encoded = urllib.parse.urlencode(params)
        url = urljoin(base=url, url=f"?{params_encoded}")
    return url


def make_request(url, verb=GET):
    logger.info(f"Starting {verb} request to {url}")
    response = requests.request(verb, url=url)
    response.raise_for_status()
    logger.info(f"Completed {verb} request to {url}")
    return response.json()
