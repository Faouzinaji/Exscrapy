# Generated by Django 3.2.16 on 2022-12-24 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_methods', '0005_price_plan_perline_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price_plan',
            name='perline_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
