# Generated by Django 4.2.11 on 2024-06-17 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_file_fileahorrovista_alter_file_filecomisiones'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='fileCrecimientoCDAT',
            field=models.FileField(default='emptyCrecimientoBase.xlsx', upload_to='uploads'),
        ),
    ]
