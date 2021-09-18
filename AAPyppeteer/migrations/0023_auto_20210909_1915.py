# Generated by Django 3.2.7 on 2021-09-09 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AAPyppeteer', '0022_alter_image_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='name',
            new_name='name_pk',
        ),
        migrations.AddField(
            model_name='project',
            name='images',
            field=models.ManyToManyField(blank=True, null=True, related_name='images', to='AAPyppeteer.Image'),
        ),
        migrations.AlterUniqueTogether(
            name='image',
            unique_together={('name_pk',)},
        ),
        migrations.RemoveField(
            model_name='image',
            name='project',
        ),
    ]
