# Generated by Django 2.1.3 on 2018-11-13 03:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0007_specialinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maininfo',
            name='burn',
        ),
        migrations.RemoveField(
            model_name='maininfo',
            name='dialysis',
        ),
        migrations.RemoveField(
            model_name='maininfo',
            name='emergency',
        ),
        migrations.RemoveField(
            model_name='maininfo',
            name='limbs',
        ),
        migrations.RemoveField(
            model_name='maininfo',
            name='newborn',
        ),
        migrations.RemoveField(
            model_name='maininfo',
            name='pregnent',
        ),
    ]
