# Generated by Django 3.2.16 on 2023-08-24 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_methods', '0008_price_plan_api_keys'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price_plan',
            name='api_keys',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]