# Generated by Django 3.1.2 on 2020-10-10 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20201010_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='completed',
            field=models.IntegerField(default=0),
        ),
    ]