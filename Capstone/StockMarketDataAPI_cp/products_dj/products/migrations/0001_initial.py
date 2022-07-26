# Generated by Django 4.0.6 on 2022-07-21 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyExchange',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('base_currency', models.CharField(default=0, max_length=3, null=True, unique=True)),
                ('change_for_currency', models.CharField(default=0, max_length=3, null=True, unique=True)),
                ('amount', models.FloatField(default=0, null=True, verbose_name='The amount to exchange')),
                ('exchanged_amount', models.FloatField(default=0, null=True, verbose_name='The amount after the exchange')),
            ],
        ),
    ]