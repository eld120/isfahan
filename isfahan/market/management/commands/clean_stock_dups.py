import json
from pathlib import Path

from django.core.management.base import BaseCommand

from isfahan.market.models import Stock


class Command(BaseCommand):
    help = "get's the most recent market data from the Market Data API"

    def handle(self, *args, **kwargs):
        fail_flag = False
        fixed = []
        all_stocks = Stock.objects.all()
        for stock in all_stocks:
            if "." in stock.ticker:
                ticker = stock.ticker
                stock.ticker = ticker.replace(".", "-")
                stock.save()
                fail_flag = True
                fixed.append(stock.ticker)
        if fail_flag:
            with Path.open("fixed_tickers.json", "w") as file:
                json.dump(fixed, file)
            self.stdout.write(self.style.SUCCESS(f"fixed {len(fixed)} stock records"))
        else:
            self.stdout.write(self.style.SUCCESS("No mistakes found"))
