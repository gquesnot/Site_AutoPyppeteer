# Generated by Django 3.2.7 on 2021-09-14 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AAPyppeteer', '0036_auto_20210914_2103'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datablock',
            old_name='user_id',
            new_name='user',
        ),
    ]
