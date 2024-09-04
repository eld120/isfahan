# Generated by Django 4.2.14 on 2024-08-22 04:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0009_stockprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockprice',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.stock', unique_for_date='date'),
        ),
    ]
