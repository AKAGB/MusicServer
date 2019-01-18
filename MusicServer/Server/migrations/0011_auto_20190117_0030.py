# Generated by Django 2.1.1 on 2019-01-17 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Server', '0010_auto_20190116_2255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlist',
            name='appuser',
        ),
        migrations.RemoveField(
            model_name='userlist',
            name='playlist',
        ),
        migrations.AddField(
            model_name='playlist',
            name='build_user',
            field=models.ForeignKey(default=1, on_delete=True, related_name='build_user', to='Server.AppUser'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='user',
            field=models.ManyToManyField(related_name='collect_user', to='Server.AppUser'),
        ),
        migrations.DeleteModel(
            name='UserList',
        ),
    ]
