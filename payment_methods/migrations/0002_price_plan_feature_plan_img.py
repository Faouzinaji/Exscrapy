# Generated by Django 3.2.16 on 2022-11-09 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_methods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='price_plan_feature',
            name='plan_img',
            field=models.ImageField(blank=True, upload_to='Plan Images', verbose_name='Plan Images'),
        ),
    ]
