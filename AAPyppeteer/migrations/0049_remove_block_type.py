# Generated by Django 3.2.7 on 2021-09-23 02:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AAPyppeteer', '0048_alter_blockconfigured_datasout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='type',
        ),
    ]
