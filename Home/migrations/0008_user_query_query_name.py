# Generated by Django 3.2.16 on 2022-12-16 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0007_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_query',
            name='query_name',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
