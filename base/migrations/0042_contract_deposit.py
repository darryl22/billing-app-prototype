# Generated by Django 4.2.1 on 2023-07-04 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0041_invoice_readingimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='deposit',
            field=models.FloatField(default=5000),
        ),
    ]
