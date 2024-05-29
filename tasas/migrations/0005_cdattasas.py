# Generated by Django 4.2.11 on 2024-05-29 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasas', '0004_cdat'),
    ]

    operations = [
        migrations.CreateModel(
            name='CdatTasas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plazoMin', models.CharField(max_length=100)),
                ('plazoMax', models.CharField(max_length=100)),
                ('valueMin', models.CharField(max_length=100)),
                ('valueMax', models.CharField(max_length=100)),
                ('tasa', models.FloatField()),
            ],
        ),
    ]
