#!/usr/bin/env python3

import sys
from argparse import ArgumentParser

from constants import CURRENCY, PORTFOLIO_FILE_PATH

from functions import (
    check_settings,
    get_sheet,
    get_summary,
    print_sheet,
    print_summary,
)


class CliParser(ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


def get_args():
    parser = CliParser()

    parser.add_argument(
        "-o",
        dest="output",
        help="What kind of output do you want: detailed or summary.",
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    options = parser.parse_args()
    if options.output not in ["detailed", "summary"]:
        parser.print_help()
        sys.exit(1)

    return options


if __name__ == "__main__":
    opts = get_args()

    check_settings(PORTFOLIO_FILE_PATH, CURRENCY)

    sheet, total = get_sheet(PORTFOLIO_FILE_PATH, CURRENCY)

    if opts.output.lower() == "detailed":
        print_sheet(sheet, CURRENCY)
    elif opts.output.lower() == "summary":
        balance_in_bitcoin, balance_in_sats = get_summary(total, CURRENCY)
        print_summary(total, balance_in_bitcoin, balance_in_sats, CURRENCY)
