# Generated by Django 2.1.1 on 2019-01-15 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Server', '0004_auto_20190115_0314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='user_name',
        ),
    ]
