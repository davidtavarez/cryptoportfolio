#!flask/bin/python

from flask import Flask, jsonify

from constants import CURRENCY, PORTFOLIO_FILE_PATH
from functions import check_settings, get_sheet, get_summary, load_portfolio

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "<h1>Hello Crypto World!</h1>"


@app.route("/api/v1/coins", methods=["GET"])
def coins():
    portfolio = load_portfolio(PORTFOLIO_FILE_PATH)
    keys = portfolio.keys()
    keys_list = list(keys)
    sorted_list_keys = sorted(keys_list)

    return jsonify(sorted_list_keys)


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
