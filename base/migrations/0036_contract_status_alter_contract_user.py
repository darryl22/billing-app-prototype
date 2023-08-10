# Generated by Django 4.2.1 on 2023-06-23 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0035_alter_contract_user_delete_paymentdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='status',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
