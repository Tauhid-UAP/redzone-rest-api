# Generated by Django 2.2 on 2021-07-30 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0006_auto_20210409_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='location',
            field=models.CharField(max_length=100),
        ),
    ]
