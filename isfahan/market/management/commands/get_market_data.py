import os
from pathlib import Path
from typing import Any

import requests
from django.core.management.base import BaseCommand
from market.models import Stock

from config.settings.base import BASE_DIR

API_DAILY_LIMIT = 90
# ruff: noqa: PTH123
MARKET_DATA_API_KEY = os.getenv("MARKET_DATA_API_KEY")


class Command(BaseCommand):
    help = "get's the most recent market data from the Market Data API"

    def handle(self, *args: Any, **options: Any) -> str | None:
        endpoint = "https://api.marketdata.app/v1/stocks/bulkquotes/?symbols="
        stocks = [stock.ticker for stock in Stock.objects.all()]
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {MARKET_DATA_API_KEY}",
        }

        url = endpoint + f"{','.join(stocks[3:103])}"

        try:
            response = requests.get(url, timeout=30, headers=headers)
            data = response.json()
            newest_stock_file = Path(f"{BASE_DIR}/newest_stock_quotes.json")
            with open(newest_stock_file, "w") as file:
                import json

                json.dump(data, file)

        except requests.RequestException as err:
            self.stdout.write(self.style.ERROR(f"WOMP WOMP can't fetch data: {err}"))
        self.stdout.write(self.style.SUCCESS("Successfully updated/created stock data"))
