import datetime
import json
from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand
from market.forms import StockImportForm
from market.models import Stock
from market.models import StockImport

from config.settings.base import BASE_DIR

# ruff: noqa: PTH123


class Command(BaseCommand):
    help = "uploads stock transactions from a local json file"

    def handle(self, *args: Any, **options: Any) -> str | None:
        upload_file = Path(f"{BASE_DIR}/newest_stock_quotes.json")
        with open(upload_file) as file:
            data = json.load(file)
        transactions = []
        transform = []
        for key, value in data.items():
            if key in ["symbol", "last", "change", "changepct", "volume", "updated"]:
                transform.append(value)
        symbol, last, change, pct, vol, update = 0, 1, 2, 3, 4, 5
        for index, _ in enumerate(transform[0]):
            transactions.append(
                (
                    transform[symbol][index],
                    transform[last][index],
                    transform[change][index],
                    transform[pct][index],
                    transform[vol][index],
                    transform[update][index],
                ),
            )
        new_transactions = []
        for symbol, last, change, percentage, volume, date in transactions:
            stock = Stock.objects.get(ticker=symbol)

            form_data = {
                "stock": stock.id,
                "price": last,
                "date": datetime.datetime.fromtimestamp(date, tz=datetime.UTC),
                "change": change,
                "change_percentage": percentage,
                "volume": volume,
            }

            form = StockImportForm(form_data)

            if form.is_valid():
                new_transactions.append(StockImport(**form.cleaned_data))
        StockImport.objects.bulk_create(new_transactions)
        self.stdout.write(self.style.SUCCESS("Successfully created stock import data"))
