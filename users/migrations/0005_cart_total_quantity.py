# Generated by Django 3.1.7 on 2021-03-26 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total_quantity',
            field=models.IntegerField(default=0),
        ),
    ]
