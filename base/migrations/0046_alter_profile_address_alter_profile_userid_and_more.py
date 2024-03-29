# Generated by Django 4.2.1 on 2023-07-27 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0045_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='userID',
            field=models.CharField(max_length=5, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='confirmationcode',
            field=models.TextField(max_length=30),
        ),
    ]
