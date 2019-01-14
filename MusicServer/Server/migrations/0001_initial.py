# Generated by Django 2.1.1 on 2019-01-14 07:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_name', models.CharField(max_length=20)),
                ('album_year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20)),
                ('reg_time', models.CharField(max_length=10)),
                ('user_place', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=20)),
                ('build_date', models.DateField()),
                ('company_place', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_name', models.CharField(max_length=20)),
                ('build_date', models.DateField()),
                ('list_label', models.CharField(max_length=20)),
                ('list_intro', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Singer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('singer_name', models.CharField(max_length=20)),
                ('singer_en_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('music_name', models.CharField(max_length=20)),
                ('music_time', models.CharField(max_length=10)),
                ('music_year', models.IntegerField()),
                ('music_style', models.CharField(max_length=10)),
                ('album_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Server.Album')),
                ('singer_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Server.Singer')),
            ],
        ),
        migrations.AddField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(to='Server.Song'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='user',
            field=models.ManyToManyField(to='Server.AppUser'),
        ),
        migrations.AddField(
            model_name='album',
            name='company_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Server.Company'),
        ),
        migrations.AddField(
            model_name='album',
            name='singer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Server.Singer'),
        ),
        migrations.AddField(
            model_name='album',
            name='users',
            field=models.ManyToManyField(to='Server.AppUser'),
        ),
    ]
