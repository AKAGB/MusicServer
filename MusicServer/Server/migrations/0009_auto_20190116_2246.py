# Generated by Django 2.1.1 on 2019-01-16 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Server', '0008_auto_20190116_2239'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='userlist',
            table='playlist_user_relationship',
        ),
    ]
