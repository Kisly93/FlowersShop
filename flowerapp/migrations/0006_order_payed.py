# Generated by Django 3.2.20 on 2023-08-19 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowerapp', '0005_auto_20230818_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payed',
            field=models.BooleanField(default=False, verbose_name='Оплачен?'),
        ),
    ]
