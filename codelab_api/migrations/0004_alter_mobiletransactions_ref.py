# Generated by Django 4.1 on 2023-02-24 14:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('codelab_api', '0003_rename_currency_countrydata_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobiletransactions',
            name='ref',
            field=models.UUIDField(verbose_name=uuid.UUID('4ff03c7b-79d1-40aa-ad9a-764c9b1f2b24')),
        ),
    ]