# Generated by Django 4.2.11 on 2024-05-27 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_asesor_cooviahorro'),
    ]

    operations = [
        migrations.CreateModel(
            name='CooviahorroMonth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameAsesor', models.CharField(max_length=100)),
                ('totalValue', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('court', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Court',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='asesor',
            name='cooviahorro',
            field=models.CharField(default='0', max_length=500),
        ),
    ]
