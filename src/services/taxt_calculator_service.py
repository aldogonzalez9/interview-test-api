import logging
import os

from .connections import build_url, make_request
from .exceptions import ExternalApiError

TAXES_OWED_PER_BAND = "taxes_owed_per_band"
MAX = "max"
MIN = "min"
RATE = "rate"

logger = logging.getLogger("tax_calculator.service")


def fix_decimals(amount):
    """Fix 2 decimals and round"""
    return round(amount, 2)


class TaxCalculatorService:
    def __init__(self) -> None:
        self.url = os.environ.get("TAX_CALCULATOR_URL")
        self.resource = os.environ.get("TAX_CALCULATOR_PATH")

    def _get_calculation_data(self, year: int):
        """'
        Request external api for tax brackets using year of taxation
        """
        try:
            logger.info("Requesting external service tax information")
            external_url = build_url(
                base_url=self.url, resource_path=f"{self.resource}/{year}"
            )
            response = make_request(url=external_url)
            logger.info("Success request for external service")
            return response
        except Exception as error:
            logger.error(error)
            raise ExternalApiError()

    def calculate(self, year: int, salary: float):
        calculation_data = self._get_calculation_data(year)
        tax_brackets = sorted(
            calculation_data["tax_brackets"], key=lambda x: x[MIN], reverse=True
        )

        remaining_taxable_salary = salary
        total_taxes = 0
        taxes_response = {TAXES_OWED_PER_BAND: []}
        while tax_brackets:
            tax_bracket = tax_brackets.pop()
            tax_bracket_min = tax_bracket[MIN]
            tax_bracket_max = tax_bracket.get(MAX, 0)
            tax_bracket_rate = tax_bracket[RATE]
            possible_amount_taxable = tax_bracket_max - tax_bracket_min
            if (
                not tax_bracket_max
                or remaining_taxable_salary < possible_amount_taxable
            ):
                real_salary_amount_taxable = remaining_taxable_salary
                remaining_taxable_salary = 0
            else:
                real_salary_amount_taxable = possible_amount_taxable
                remaining_taxable_salary -= possible_amount_taxable

            tax_payable = real_salary_amount_taxable * tax_bracket_rate
            total_taxes += tax_payable
            current_band = {
                "tax_bracket": f"{tax_bracket_min}-{tax_bracket_max}",
                "marginal_tax_rate": f"{tax_bracket_rate}",
                "amount_taxable": fix_decimals(real_salary_amount_taxable),
                "tax_payable": fix_decimals(tax_payable),
            }
            taxes_response[TAXES_OWED_PER_BAND].append(current_band)
        taxes_response["total_taxes_owed"] = fix_decimals(total_taxes)
        taxes_response["salary"] = fix_decimals(salary)
        taxes_response["tax_year"] = year

        return taxes_response
