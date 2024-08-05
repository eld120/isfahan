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
    ticker = models.CharField(max_length=6)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.ticker)
        super(Stock, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
    



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

    stock = models.ForeignKey("market.Stock", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField(auto_now=False, auto_now_add=False)
    change = models.DecimalField(max_digits=5, decimal_places=2)
    change_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    volume = models.IntegerField()
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.stock} {self.date}')
        super(StockImport, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.stock} {self.date}"
    