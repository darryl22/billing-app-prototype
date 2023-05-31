# Generated by Django 4.2 on 2023-04-26 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_utility_supplier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utility',
            name='supplier',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='supplier', to='base.profile'),
        ),
    ]