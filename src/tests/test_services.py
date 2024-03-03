import pytest
import requests_mock

from src.services.taxt_calculator_service import TaxCalculatorService
from src.tests.mocks import tax_brackets_2022
from src.services.exceptions import ExternalApiError


class TestServices(object):
    def test_get_calculation_data(self):
        with requests_mock.mock() as m:
            m.get(requests_mock.ANY, status_code=200, json=tax_brackets_2022)

            tax_calculator = TaxCalculatorService()
            response = tax_calculator._get_calculation_data("2022")

        assert response == tax_brackets_2022, "Expexted tax_brackets not received"

    def test_get_calculation_data_error(self):
        with requests_mock.mock() as m:
            m.get(requests_mock.ANY, status_code=500, text="database error")
            tax_calculator = TaxCalculatorService()
            with pytest.raises(ExternalApiError):
                tax_calculator._get_calculation_data("2022")

    @pytest.mark.parametrize(
        "salary, expected_total_taxes",
        [(0, 0), (50000, 7500), (100000, 17739.17), (1234567, 385587.65)],
    )
    def test_salary_tax_calculation(self, salary, expected_total_taxes):
        with requests_mock.mock() as m:
            m.get(requests_mock.ANY, status_code=200, json=tax_brackets_2022)
            tax_calculations = TaxCalculatorService().calculate(2022, salary)
            assert (
                tax_calculations["total_taxes_owed"] == expected_total_taxes
            ), f"{expected_total_taxes} was expected but received {tax_calculations['total_taxes_owed']}"
