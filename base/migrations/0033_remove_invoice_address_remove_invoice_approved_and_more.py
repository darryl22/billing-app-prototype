# Generated by Django 4.2.1 on 2023-06-12 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0032_invoice_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='address',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='receiverAddress',
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoiceNo',
            field=models.PositiveIntegerField(null=True, unique=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='prepayment',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='invoice',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='year',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='amountpayable',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='arrears',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='billingmonth',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='consumed',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='consumptionamount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='currentreading',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='previousreading',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
