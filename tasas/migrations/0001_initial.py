# Generated by Django 4.2.11 on 2024-05-16 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Afiliaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('rol', models.CharField(max_length=200)),
                ('since', models.IntegerField()),
                ('until', models.IntegerField()),
                ('value', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Colocaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('rol', models.CharField(max_length=200)),
                ('tasa_min', models.CharField(max_length=20)),
                ('tasa_max', models.CharField(max_length=20)),
                ('value_min', models.CharField(max_length=100)),
                ('value_max', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=50)),
            ],
        ),
    ]
