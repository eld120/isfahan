# ruff: noqa: BLE001
from django.core.management.base import BaseCommand

from isfahan.market.models import Stock
from isfahan.market.models import StockPrice


class Command(BaseCommand):
    help = "updates the previous attribute for a StockPrice object"

    def handle(self, *args, **kwargs):
        all_stocks = [stock.id for stock in Stock.objects.all()]
        try:
            for pk in all_stocks:
                all_prices = StockPrice.objects.filter(stock__id=pk).order_by("date")
                update_list = []
                previous = None
                for index, price in enumerate(all_prices):
                    if index > 0:
                        price.previous = previous
                        update_list.append(price)
                    previous = price
                StockPrice.objects.bulk_update(update_list, ["previous"])

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"It smells like your computer is burning: {e}"),
            )

        self.stdout.write(
            self.style.SUCCESS("Successfully updated stock prices maybe..."),
        )
