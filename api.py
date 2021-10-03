#!flask/bin/python

from flask import Flask, jsonify

from constants import CURRENCY, PORTFOLIO_FILE_PATH
from functions import (
    check_settings,
    get_sheet,
    get_summary,
)

app = Flask(__name__)


@app.route("/api/v1/sheet", methods=["GET"])
def sheet():
    table, total = get_sheet(PORTFOLIO_FILE_PATH, CURRENCY)

    sheet = []
    for coin in table:
        sheet.append(
            {"name": coin[0], "coins": coin[1], "price": coin[2], "balance": coin[3]}
        )

    return jsonify(
        {
            "results": sheet,
            "currency": CURRENCY.upper(),
        }
    )


@app.route("/api/v1/summary", methods=["GET"])
def summary():
    table, total = get_sheet(PORTFOLIO_FILE_PATH, CURRENCY)

    balance_in_bitcoin, balance_in_sats = get_summary(total, CURRENCY)

    return jsonify(
        {
            "results": {
                "bitcoin": balance_in_bitcoin,
                "total": total,
                "sats": balance_in_sats,
            },
            "currency": CURRENCY.upper(),
        }
    )


if __name__ == "__main__":
    check_settings(PORTFOLIO_FILE_PATH, CURRENCY)

    app.run(debug=True, host="0.0.0.0")
