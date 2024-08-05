from typing import Any
import requests, csv
from django.core.management.base import BaseCommand
from .models import Stock, StockImport
from .forms import StockForm, StockImportForm


class MarketCommand(BaseCommand):
    help = "get's the most recent market data from the Market Data API"
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        endpoint = "https://api.marketdata.app/v1/stocks/bulkquotes/"
        stocks = []
        top_99 = []
        with open(r'C:/Users/seyam/Downloads/stocks_2.csv', 'r') as f:
            file = csv.DictReader(f)
            for line in file:
                if int(line['no']) < 100:
                    top_99.append((line['name'], line['ticker']))
                stocks.append((line['name'], line['ticker']))
        stocks_to_create = []
        for name, ticker in stocks:
            form_data = {
                'ticker' : ticker.UPPER(),
                'name' : name,
                
                         }
            form = StockForm(form_data)
            if form.is_valid():
                try:
                    Stock.objects.get(ticker=form.cleaned_data['ticker'])
                except Stock.DoesNotExist:
                    stocks_to_create.append(Stock(**form.cleaned_data))
        Stock.objects.bulk_create(stocks_to_create)


        url = endpoint + f"{','.join([x[1] for x in stocks])}"
        try:
            response = requests.get(url)
            data = response.json()
        except requests.RequestException as err:
            self.stdout.write(self.style.ERROR(f"WOMP WOMP can't fetch data: {err}"))
        self.stdout.write(self.style.SUCCESS('Successfully updated/created stock data'))
        return super().handle(*args, **options)