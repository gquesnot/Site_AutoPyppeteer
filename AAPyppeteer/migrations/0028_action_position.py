# Generated by Django 3.2.7 on 2021-09-12 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AAPyppeteer', '0027_alter_block_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='position',
            field=models.IntegerField(default=0),
        ),
    ]
