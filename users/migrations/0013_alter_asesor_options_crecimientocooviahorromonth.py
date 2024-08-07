# Generated by Django 4.2.11 on 2024-06-26 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_countcrecimientocdat'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asesor',
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='CrecimientoCooviahorroMonth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.sucursale')),
            ],
            options={
                'ordering': ['-year', '-month'],
            },
        ),
    ]
