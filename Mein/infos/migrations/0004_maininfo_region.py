# Generated by Django 2.1.3 on 2018-11-08 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0003_auto_20181108_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='maininfo',
            name='region',
            field=models.CharField(default='', max_length=20),
        ),
    ]