# Generated by Django 3.1 on 2020-08-23 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='releaseyear',
        ),
        migrations.AddField(
            model_name='movie',
            name='url',
            field=models.TextField(db_index=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='writers',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='year',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movie',
            name='image',
            field=models.TextField(blank=True),
        ),
    ]
