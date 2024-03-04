# Project Title

Tax calculator service 

## Description

Accomplish the following:
* Calculate taxes by year [2019|2020|2021|2022]
* Receive a yearly salary i.e. /api/taxes/years/2022?salary=100000
* Calculate and display the total taxes owed for the salary
* Display the amount of taxes owed per band
* Display the effective rate

Sample response:
```
{
    "salary": 100000,
    "tax_year": 2022,
    "taxes_owed_per_band": [
        {
            "amount_taxable": 50197,
            "marginal_tax_rate": "0.15",
            "tax_bracket": "0-50197",
            "tax_payable": "7529.55"
        },
        {
            "amount_taxable": 49803,
            "marginal_tax_rate": "0.205",
            "tax_bracket": "50197-100392",
            "tax_payable": "10209.61"
        },
        {
            "amount_taxable": 0,
            "marginal_tax_rate": "0.26",
            "tax_bracket": "100392-155625",
            "tax_payable": "0.0"
        },
        {
            "amount_taxable": 0,
            "marginal_tax_rate": "0.29",
            "tax_bracket": "155625-221708",
            "tax_payable": "0.0"
        },
        {
            "amount_taxable": 0,
            "marginal_tax_rate": "0.33",
            "tax_bracket": "221708-0",
            "tax_payable": "0.0"
        }
    ],
    "total_taxes_owed": 17739.17
}
```

## Getting Started

### Dependencies
* Python 3

### Installing

* Clone this repository and later create virtualenv for the project,after that you can install requirements
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create local .env file with these variables: 

```
TAX_CALCULATOR_URL = 'http://servername'
TAX_CALCULATOR_PATH = '/tax-calculator/tax-year'
```

### Executing program

* Run the following command in project folder
```
python app.py
```

## Run tests

```
python -m pytest
```

## Authors

Aldo Gonzalez

## Help

You can use X-Trace-Id in headers to find related logs

Docker configuration pending.