# Generated by Django 4.2.1 on 2023-06-05 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_profile_prepayment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reading',
            name='reading',
            field=models.FloatField(),
        ),
    ]
