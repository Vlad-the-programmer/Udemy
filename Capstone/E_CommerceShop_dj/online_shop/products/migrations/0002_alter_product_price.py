# Generated by Django 4.0.6 on 2022-07-28 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(max_length=4, null=True, verbose_name='A price'),
        ),
    ]
