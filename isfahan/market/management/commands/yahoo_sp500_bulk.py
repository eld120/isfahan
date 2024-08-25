import json
from pathlib import Path

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
        failed_transactions = []
        fail_flag = False
        for k, v in data.items():
            ticker, timestamp = k
            form = StockPriceForm(
                {
                    "stock": v["stock"],
                    "price": round(v["price"], 4),
                    "date": timestamp,
                    "volume": v["volume"],
                },
            )
            if form.is_valid():
                new_transactions.append(StockPrice(**form.cleaned_data))
            else:
                fail_flag = True
                failed_transactions.append(
                    {
                        "stock": v["stock"],
                        "price": v["price"],
                        "date": timestamp.to_pydatetime().strftime("%m/%d/%Y"),
                        "volume": v["volume"],
                        "erros": form.errors,
                    },
                )
        if fail_flag:
            with Path.open("failed_transactions.json", "w") as file:
                json.dump(failed_transactions, file)
        StockPrice.objects.bulk_create(new_transactions)
        self.stdout.write(self.style.SUCCESS("Successfully created stock price data"))
