from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.text import slugify

# Create your models here.


class Stock(models.Model):
    """
    Stock Data from the Market Data API -> Stock Model

    name : User Defined/Provided
    symbol : ticker

    """

    name = models.CharField(max_length=50)
    ticker = models.CharField(max_length=6, unique=True)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.ticker)
        super().save(*args, **kwargs)


class StockImport(models.Model):
    """
    Represents a Stock price at a given time
    Import Stock data from the Market Data API -> StockImport Model

    stock : get_model_or_404(symbol, Stock) # something like this
    price : last
    date : updated
    change : change
    change_percentage : changepct
    volume : volume
    """

    stock = models.ForeignKey(
        "market.Stock",
        on_delete=models.CASCADE,
        unique_for_date="price",
    )
    price = models.DecimalField(max_digits=19, decimal_places=4)
    date = models.DateField(auto_now=False, auto_now_add=False)
    change = models.DecimalField(max_digits=19, decimal_places=4)
    change_percentage = models.DecimalField(max_digits=10, decimal_places=4)
    volume = models.IntegerField()
    slug = models.SlugField(blank=True)

    def __str__(self):
        return f"{self.stock} {self.date}"

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.id} {self.stock} {self.date}")
        super().save(*args, **kwargs)


class StockPrice(models.Model):
    """
    Represents a Stock price at a given time
    Import Stock data from the Market Data API -> StockImport Model

    stock : get_model_or_404(symbol, Stock) # something like this
    price : Close
    date : Timestamp
    volume : volume
    """

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
