# Generated by Django 4.2.11 on 2024-06-24 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_file_filecrecimientoahorro_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrecimientoCdatMonth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.sucursale')),
            ],
        ),
    ]
