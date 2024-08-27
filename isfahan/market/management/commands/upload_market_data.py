import datetime
import logging
from pathlib import Path
from typing import Any

import pandas as pd
from django.core.management.base import BaseCommand
from market.forms import StockImportForm
from market.models import Stock
from market.models import StockImport

from config.settings.base import BASE_DIR

# ruff: noqa: PTH123
logger = logging.Logger()


class Command(BaseCommand):
    help = "uploads stock transactions from a local json file"

    def handle(self, *args: Any, **options: Any) -> str | None:
        data = pd.read_json(Path(f"{BASE_DIR}/newest_stock_quotes.json"))

        new_transactions = []
        for _, row in data.iterrows():
            stock = Stock.objects.get(ticker=row["symbol"])

            form_data = {
                "stock": stock.id,
                "price": row["last"],
                "date": datetime.datetime.fromtimestamp(
                    row["updated"],
                    tz=datetime.UTC,
                ),
                "change": row["change"],
                "change_percentage": row["changepct"],
                "volume": row["volume"],
            }

            form = StockImportForm(form_data)

            if form.is_valid():
                new_transactions.append(StockImport(**form.cleaned_data))
        StockImport.objects.bulk_create(new_transactions)
        self.stdout.write(self.style.SUCCESS("Successfully created stock import data"))
