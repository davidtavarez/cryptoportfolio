import collections
import json
import sys
from pathlib import Path

from pycoingecko import CoinGeckoAPI
from tabulate import tabulate

from constants import COINFRACTION


def check_settings(portfolio_file, currency):
    if not Path(portfolio_file).exists():
        sys.exit("ERROR: No portfolio loaded!")

    valid_currency, supported = validate_currency(currency)
    if not valid_currency:
        sys.exit(f"ERROR: Currency not valid. Valid currencies: {', '.join(supported)}")


def load_portfolio(file_path="./portfolio.json"):
    with open(file_path) as f:
        return json.load(f, object_pairs_hook=collections.OrderedDict)


def validate_currency(currency):
    supported = CoinGeckoAPI().get_supported_vs_currencies()
    if currency not in supported:
        return False, supported

    return True, None


def get_prices(portfolio, currency):
    return CoinGeckoAPI().get_price(
        ids=",".join([crypto for crypto in portfolio]), vs_currencies=currency
    )


def get_balances_sheet(portfolio, prices, currency):
    table = []
    total = 0

    for crypto in sorted(portfolio.keys()):
        name = crypto.replace("-", " ").title()
        price = prices[crypto][currency]
        coins = portfolio[crypto]
        balance = prices[crypto][currency] * portfolio[crypto]

        total += balance

        table.append(
            [
                name,
                coins,
                price,
                balance,
            ]
        )

    return table, total


def get_sheet(portfolio_file, currency):
    portfolio = load_portfolio(portfolio_file)
    prices = get_prices(portfolio, currency)
    return get_balances_sheet(portfolio, prices, currency)


def print_sheet(table, currency):
    print(
        tabulate(
            table,
            headers=[
                "NAME",
                "COINS",
                f"PRICE ({currency.upper()})",
                f"BALANCE ({currency.upper()})",
            ],
            tablefmt="fancy_grid",
            numalign="right",
            floatfmt=[None, ",.9f", ",.2f", ",.2f"],
        )
    )


def get_summary(total, currency):
    bitcoin_price = CoinGeckoAPI().get_price(ids="bitcoin", vs_currencies=[currency])

    balance_in_bitcoin = total / bitcoin_price["bitcoin"][currency]
    balance_in_sats = balance_in_bitcoin / COINFRACTION

    return balance_in_bitcoin, balance_in_sats


def print_summary(total, balance_in_bitcoin, balance_in_sats, currency):
    table = [
        ["Bitcoin", f"{balance_in_bitcoin}"],
        [f"Balance ({currency.upper()})", f"{total:,.2f}"],
        ["Satoshis (SAT)", f"{balance_in_sats:,}"],
    ]
    print(
        tabulate(
            table,
            tablefmt="fancy_grid",
            disable_numparse=True,
        )
    )
