# Generated by Django 4.2.11 on 2024-03-26 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asesor',
            name='rol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roles.roles'),
        ),
    ]