# Generated by Django 3.2.7 on 2021-09-05 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AAPyppeteer', '0008_auto_20210905_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='name',
            field=models.CharField(default=1234, max_length=200),
            preserve_default=False,
        ),
    ]
