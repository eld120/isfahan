# ruff: noqa: BLE001
from django.core.management.base import BaseCommand

from isfahan.market.models import Stock
from isfahan.market.models import StockPrice


class Command(BaseCommand):
    help = "get's the most recent market data from the Market Data API"

    def handle(self, *args, **kwargs):
        all_stocks = Stock.objects.all()
        try:
            for stock in all_stocks:
                all_prices = StockPrice.objects.filter(stock=stock).order_by("date")
                previous = None
                for index, price in enumerate(all_prices):
                    if index > 0:
                        StockPrice.objects.filter(id=price.id).update(previous=previous)
                    previous = price

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"It smells like your computer is burning: {e}"),
            )

        self.stdout.write(
            self.style.SUCCESS("Successfully updated stock prices maybe..."),
        )
