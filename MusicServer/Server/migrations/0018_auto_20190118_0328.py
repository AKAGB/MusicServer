# Generated by Django 2.1.1 on 2019-01-18 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Server', '0017_auto_20190118_0318'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='album_id',
            new_name='album',
        ),
        migrations.RenameField(
            model_name='song',
            old_name='singer_id',
            new_name='singer',
        ),
    ]
