import logging
from marshmallow import fields, Schema, ValidationError, validate
from flask import Response

logger = logging.getLogger("tax_calculator.schemas")


class SchemaParamsValidationError(Exception):
    description = "Params Validation Error"
    code = 400
    error_trace = ""

    def __init__(self, error_trace: str, *args: object) -> None:
        super().__init__(*args)
        if error_trace:
            self.error_trace = error_trace

    def get_response(self):
        return Response(str(self), self.code)


def validate_request_params(params, schema):
    try:
        return schema().load(params)
    except ValidationError as e:
        logger.error(e)
        raise SchemaParamsValidationError(error_trace=str(e))


class TaxCalulcatorParamsSchema(Schema):
    salary = fields.Int(description="Salary to calculate owed taxes.", required=True)


class TaxCalulcatorPathParamsSchema(Schema):
    year = fields.Int(
        description="The year of tax calculation",
        validate=validate.Range(min=2019, max=2022),
        required=True,
    )


def validate_tax_calculator_params(request):
    path_params_validation = validate_request_params(
        request.view_args, TaxCalulcatorPathParamsSchema
    )
    params_validation = validate_request_params(request.args, TaxCalulcatorParamsSchema)
    return {**path_params_validation, **params_validation}
