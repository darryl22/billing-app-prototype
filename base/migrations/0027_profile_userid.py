# Generated by Django 4.2.1 on 2023-06-02 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_utility_connectiondate'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='userID',
            field=models.CharField(null=True, unique=True),
        ),
    ]
