# Generated by Django 4.2.11 on 2024-06-04 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0001_initial'),
        ('tasas', '0006_ahorrovista'),
    ]

    operations = [
        migrations.CreateModel(
            name='CdatCaptaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('type', models.CharField(choices=[('nuevo', 'Nuevo'), ('renovado', 'Renovado')], max_length=100)),
                ('valueMin', models.CharField(max_length=100)),
                ('valueMax', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roles.roles')),
            ],
        ),
    ]
