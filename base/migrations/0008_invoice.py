# Generated by Django 4.2 on 2023-04-25 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_utility_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=20)),
                ('receiver', models.CharField(max_length=30)),
                ('receiverAddress', models.CharField(max_length=30)),
                ('billingmonth', models.CharField(max_length=30)),
                ('previousreading', models.CharField(max_length=20)),
                ('currentreading', models.CharField(max_length=20)),
                ('consumed', models.CharField(max_length=20)),
                ('rate', models.CharField(max_length=20)),
                ('consumptionamount', models.CharField(max_length=20)),
                ('arrears', models.CharField(max_length=20)),
                ('amountpayable', models.CharField(max_length=20)),
            ],
        ),
    ]
