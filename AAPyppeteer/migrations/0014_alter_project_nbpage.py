# Generated by Django 3.2.7 on 2021-09-05 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AAPyppeteer', '0013_alter_project_datas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='nbPage',
            field=models.IntegerField(default=0),
        ),
    ]
