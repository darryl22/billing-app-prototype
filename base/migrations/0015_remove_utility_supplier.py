# Generated by Django 4.2 on 2023-04-26 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_utility_supplier'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utility',
            name='supplier',
        ),
    ]
