from flask import request, Response, json, Blueprint
import logging

from src.services.taxt_calculator_service import TaxCalculatorService

logger = logging.getLogger(__name__)

taxes = Blueprint("taxes", __name__)


@taxes.route("/years/<int:year>", methods=["GET"])
def handle_tax_calculation_by_year(year):
    logger.info("Starting Tax calculation")
    args = request.args
    salary = int(args["salary"])
    calculation = TaxCalculatorService().calculate(year=year, salary=salary)
    logger.info("Tax calculation Completed")
    return Response(
        response=json.dumps(calculation), status=200, mimetype="application/json"
    )
