from typing import Any

from django.core.management.base import BaseCommand
from market.models import StockImport

# ruff: noqa: PTH123


class Command(BaseCommand):
    help = "uploads stock transactions from a local json file"

    def handle(self, *args: Any, **options: Any) -> str | None:
        all_stock_transactions = StockImport.objects.all()
        unique_transactions = set()
        count = 0
        for stock in all_stock_transactions:
            if (stock.stock.ticker, stock.date) in unique_transactions:
                count += 1
                stock.delete()
            else:
                unique_transactions.add((stock.stock.ticker, stock.date))

        success_string = (
            f"Successfully removed {count} duplicate records"
            if count > 0
            else "No Duplicates Found"
        )
        self.stdout.write(self.style.SUCCESS(success_string))
