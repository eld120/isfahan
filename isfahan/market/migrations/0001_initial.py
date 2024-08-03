# Generated by Django 4.2.14 on 2024-07-28 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('ticker', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StockTransactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date', models.DateField()),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.stock')),
            ],
        ),
    ]
