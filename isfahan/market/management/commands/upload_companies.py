from pathlib import Path

from django.core.management.base import BaseCommand

from isfahan.market.forms import StockForm


class Command(BaseCommand):
    help = "get's the most recent market data from the Market Data API"

    def handle(self, *args, **kwargs):
        with Path.open(
            "C:/Users/seyam/Sandbox/isfahan_local/isfahan/companies.csv",
        ) as file:
            for line in file:
                row = line.rstrip("\n").split("\t")
                ticker, company = row[1], row[2]
                if "." in ticker:
                    ticker.replace(".", "-")

                form = StockForm({"name": company, "ticker": ticker})
                if form.is_valid():
                    form.save()
