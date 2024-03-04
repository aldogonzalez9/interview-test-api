import logging

from flask import request, Response, json, Blueprint

from src.services.taxt_calculator_service import TaxCalculatorService
from src.schemas import validate_tax_calculator_params

logger = logging.getLogger(__name__)

taxes = Blueprint("taxes", __name__)


@taxes.route("/years/<int:year>", methods=["GET"])
def handle_tax_calculation_by_year(year):
    logger.info("Starting Tax calculation")
    validation_result = validate_tax_calculator_params(request)
    logger.info(f"Validation result: {validation_result}")
    salary = validation_result["salary"]
    calculation = TaxCalculatorService().calculate(year=year, salary=salary)
    logger.info("Tax calculation Completed")
    return Response(
        response=json.dumps(calculation), status=200, mimetype="application/json"
    )
