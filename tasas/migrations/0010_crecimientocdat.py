# Generated by Django 4.2.11 on 2024-06-17 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasas', '0009_delete_cdatcaptaciones'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrecimientoCDAT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medida', models.CharField(max_length=100)),
                ('tasaMin', models.FloatField()),
                ('tasaMax', models.FloatField()),
                ('comision', models.CharField(max_length=100)),
            ],
        ),
    ]
