# Generated by Django 3.2.16 on 2023-07-03 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[(1, 'Mail'), (2, 'Femail')], max_length=25, null=True, verbose_name='Gender'),
        ),
    ]
