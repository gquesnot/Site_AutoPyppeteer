# Generated by Django 3.2.7 on 2021-09-09 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AAPyppeteer', '0021_image'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='image',
            unique_together={('name', 'project')},
        ),
    ]
