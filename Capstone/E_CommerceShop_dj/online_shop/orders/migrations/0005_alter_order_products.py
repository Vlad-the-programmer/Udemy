# Generated by Django 4.1 on 2022-09-22 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
        ('orders', '0004_alter_order_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='products', to='products.product', verbose_name='Ordered products'),
        ),
    ]
