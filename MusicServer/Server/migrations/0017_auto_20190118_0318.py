# Generated by Django 2.1.1 on 2019-01-18 03:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Server', '0016_auto_20190117_0103'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='company_id',
            new_name='company',
        ),
    ]
