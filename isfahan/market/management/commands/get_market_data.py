import csv
from pathlib import Path
from typing import Any

import requests
from django.core.management.base import BaseCommand
from market.forms import StockForm
from market.models import Stock

from config.settings.base import BASE_DIR

API_DAILY_LIMIT = 100
# ruff: noqa: PTH123


class MarketCommand(BaseCommand):
    help = "get's the most recent market data from the Market Data API"

    def handle(self, *args: Any, **options: Any) -> str | None:
        endpoint = "https://api.marketdata.app/v1/stocks/bulkquotes/"
        stocks = []
        top_99 = []
        # initial load of companies into the DB
        stock_file = Path(r"C:/Users/seyam/Downloads/stocks_2.csv")

        with open(stock_file) as f:
            file = csv.DictReader(f)
            for line in file:
                if int(line["no"]) < API_DAILY_LIMIT:
                    top_99.append((line["name"], line["ticker"]))
                stocks.append((line["name"], line["ticker"]))
        stocks_to_create = []
        for name, ticker in stocks:
            form_data = {
                "ticker": ticker.upper(),
                "name": name,
            }
            form = StockForm(form_data)
            if form.is_valid():
                try:
                    Stock.objects.get(ticker=form.cleaned_data["ticker"])
                except Stock.DoesNotExist:
                    stocks_to_create.append(Stock(**form.cleaned_data))
        Stock.objects.bulk_create(stocks_to_create)

        url = endpoint + f"{','.join([x[1] for x in stocks])}"
        try:
            response = requests.get(url, timeout=30)
            data = response.json()
            newest_stock_file = Path(f"{BASE_DIR}/newest_stock_quotes.json")
            with open(newest_stock_file, "w") as file:
                import json

                json.dump(data, file)

        except requests.RequestException as err:
            self.stdout.write(self.style.ERROR(f"WOMP WOMP can't fetch data: {err}"))
        self.stdout.write(self.style.SUCCESS("Successfully updated/created stock data"))
