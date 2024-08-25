import yfinance as yf
from django.core.management.base import BaseCommand

from isfahan.market.forms import StockPriceForm
from isfahan.market.models import Stock
from isfahan.market.models import StockPrice


class Command(BaseCommand):
    help = "get's the most recent market data from the Market Data API"

    def handle(self, *args, **kwargs):
        sp100 = {stock.ticker: stock.id for stock in Stock.objects.all()}
        # handle errors below
        top_100 = yf.download(
            [ticker for ticker, _ in sp100.items()],
            period="5d",
        ).to_dict()

        data = {}
        for key, val in top_100.items():
            noun, ticker = key
            if noun in ("Close", "Volume"):
                for timestamp, value in val.items():
                    if (ticker, timestamp) not in data:
                        data[(ticker, timestamp)] = {
                            "price" if noun == "Close" else "volume": value,
                        }
                        data[(ticker, timestamp)]["stock"] = sp100[ticker]
                    else:
                        data[(ticker, timestamp)][
                            "price" if noun == "Close" else "volume"
                        ] = value
        new_transactions = []
        for k, v in data.items():
            ticker, timestamp = k
            form = StockPriceForm(
                {
                    "stock": v["stock"],
                    "price": v["price"],
                    "date": timestamp,
                    "volume": v["volume"],
                },
            )
            if form.is_valid():
                new_transactions.append(StockPrice(**form.cleaned_data))
        StockPrice.objects.bulk_create(new_transactions)
        self.stdout.write(self.style.SUCCESS("Successfully created stock price data"))
