# isfahan

A Django powered paper trading platform

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy isfahan

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd isfahan
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd isfahan
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd isfahan
celery -A config.celery_app worker -B -l info
```

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [Mailpit](https://github.com/axllent/mailpit) with a web interface is available as docker container.

Container mailpit will start automatically when you will run all docker containers.
Please check [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html) for more details how to start all containers.

With Mailpit running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

I have a google finance clone project and I need help refactoring the management command that I use to download/update the most recent market data using the `yfinance` library. Here are the Stock (represents a company and stock ticker) and StockPrice (represents a company's stock price on a given day) models:

```python
# models.py
class Stock(models.Model):
    name = models.CharField(max_length=50)
    ticker = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class StockPrice(models.Model):
    stock = models.ForeignKey(
        "market.Stock",
        on_delete=models.CASCADE,
        unique_for_date="date",
    )
    previous = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=19, decimal_places=4)
    date = models.DateField(auto_now=False, auto_now_add=False)
    volume = models.IntegerField()

    def __str__(self):
        return f"{self.stock} {self.date}"

    def save(self, *args, **kwargs):
        try:
            previous_date = self.objects.values("date").distinct().order_by("-date")[0]
            self.previous = self.objects.get(stock=self.stock, date=previous_date)
        except ObjectDoesNotExist:
            pass
        super().save(*args, **kwargs)
```

I've chosen to calculate the difference in stock prices by storing a reference to the previous day's stock price on every StockPrice record. The management command I have does not update/populate the `self.previous` attribute on the new `StockPrice` records because I'm using the `bulk_create()` method. I need you to refactor my `market_download` management command to populate/update all fields on the StockPrice model and ideally while still using the `bulk_create` method.

```python
# management/commands/market_download.py
class Command(BaseCommand):
    help = "get's the most recent market data from Yahoo Finance via the yfinance library"

    def handle(self, *args, **kwargs):
        all_stocks = {stock.ticker: stock.id for stock in Stock.objects.all()}

        top_100 = yf.download(
            [ticker for ticker, _ in all_stocks.items()],
            period="5d",
        ).to_dict()

        data = {}

        for key, val in top_100.items():
            noun, ticker = key
            if "." in ticker:
                ticker = ticker.replace(".", "-")
            if noun in ("Close", "Volume"):
                for timestamp, value in val.items():
                    if (ticker, timestamp) not in data:
                        data[(ticker, timestamp)] = {
                            "price" if noun == "Close" else "volume": value,
                        }
                        data[(ticker, timestamp)]["stock"] = all_stocks[ticker]
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
        StockPrice.objects.bulk_create(new_transactions, batch_size=500)
        self.stdout.write(self.style.SUCCESS("Successfully created stock price data"))
```
