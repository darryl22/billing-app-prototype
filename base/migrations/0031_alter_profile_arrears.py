# Generated by Django 4.2.1 on 2023-06-12 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0030_profile_previousarrears'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='arrears',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
