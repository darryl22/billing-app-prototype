# Generated by Django 4.2.1 on 2023-06-19 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0033_remove_invoice_address_remove_invoice_approved_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reading',
            options={'get_latest_by': 'created'},
        ),
    ]