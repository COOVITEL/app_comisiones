# Generated by Django 4.2.11 on 2024-05-22 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colocaciones',
            name='value_max',
            field=models.CharField(max_length=100, null=True),
        ),
    ]