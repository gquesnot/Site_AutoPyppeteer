# Generated by Django 3.2.7 on 2021-09-07 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AAPyppeteer', '0015_alter_project_nbpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='core',
        ),
        migrations.RemoveField(
            model_name='project',
            name='datas',
        ),
        migrations.RemoveField(
            model_name='project',
            name='init',
        ),
        migrations.RemoveField(
            model_name='project',
            name='nbPage',
        ),
        migrations.CreateModel(
            name='BlockConfigured',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('nbThread', models.IntegerField(default=0)),
                ('datas', models.JSONField(default=list)),
                ('block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AAPyppeteer.block')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='blocks',
            field=models.ManyToManyField(blank=True, null=True, related_name='blocks', to='AAPyppeteer.BlockConfigured'),
        ),
    ]
