# Generated by Django 4.0.2 on 2022-02-12 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_test_total_words'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_id', models.IntegerField(db_index=True)),
                ('word', models.CharField(db_index=True, max_length=50)),
                ('answer', models.CharField(max_length=50)),
                ('rank', models.IntegerField()),
            ],
        ),
    ]
