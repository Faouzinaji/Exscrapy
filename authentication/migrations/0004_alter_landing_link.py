# Generated by Django 3.2.16 on 2023-07-09 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_features_landing_price_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landing',
            name='link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
