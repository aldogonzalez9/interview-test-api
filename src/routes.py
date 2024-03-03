from flask import Blueprint
from src.controllers.tax_calculator_controller import taxes

api = Blueprint("api", __name__)

api.register_blueprint(taxes, url_prefix="/taxes")
