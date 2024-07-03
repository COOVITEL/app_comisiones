# Generated by Django 4.2.11 on 2024-07-03 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasas', '0011_crecimientocooviahorro'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrecimientoAhorroVista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
                ('valueMin', models.CharField(max_length=500)),
                ('valueMax', models.CharField(max_length=500)),
                ('porcentaje', models.FloatField()),
            ],
        ),
    ]
