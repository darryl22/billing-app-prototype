# Generated by Django 4.2 on 2023-05-04 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_remove_reading_meternumber_utility_meternumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bankname', models.CharField(max_length=30)),
                ('bankbranch', models.CharField(max_length=30)),
                ('bankaccountno', models.CharField(max_length=30)),
                ('bankaccountname', models.CharField(max_length=30)),
                ('swiftcode', models.CharField(max_length=20)),
                ('paybillno', models.CharField(max_length=15)),
                ('paybillaccountno', models.CharField(max_length=20)),
                ('name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='base.profile')),
            ],
        ),
    ]
