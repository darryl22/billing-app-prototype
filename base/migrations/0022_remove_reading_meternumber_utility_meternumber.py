# Generated by Django 4.2 on 2023-04-27 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_reading_meternumber_contract'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reading',
            name='meternumber',
        ),
        migrations.AddField(
            model_name='utility',
            name='meternumber',
            field=models.CharField(max_length=30, null=True),
        ),
    ]