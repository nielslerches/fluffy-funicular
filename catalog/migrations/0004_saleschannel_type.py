# Generated by Django 2.2.6 on 2019-10-24 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20191024_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleschannel',
            name='type',
            field=models.CharField(default='online shop', max_length=255),
        ),
    ]
