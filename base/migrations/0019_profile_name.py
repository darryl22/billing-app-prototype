# Generated by Django 4.2 on 2023-04-26 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_alter_utility_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default='', max_length=20),
        ),
    ]
