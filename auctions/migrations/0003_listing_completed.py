# Generated by Django 4.1.4 on 2022-12-27 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='completed',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
