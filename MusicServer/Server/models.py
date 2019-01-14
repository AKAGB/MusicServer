from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20)
    reg_time = models.CharField(max_length=10)
    user_place = models.CharField(max_length=20)

class Singer(models.Model):
    singer_name = models.CharField(max_length=20)
    singer_en_name = models.CharField(max_length=20)

class Company(models.Model):
    company_name = models.CharField(max_length=20)
    build_date = models.DateField()
    company_place = models.CharField(max_length=20)

class Album(models.Model):
    album_name = models.CharField(max_length=20)
    album_year = models.IntegerField()
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE, default=1)

    # Relationship set
    users = models.ManyToManyField(AppUser)

class Song(models.Model):
    music_name = models.CharField(max_length=20)
    music_time = models.CharField(max_length=10)
    music_year = models.IntegerField()
    music_style = models.CharField(max_length=10)
    singer_id = models.ForeignKey(Singer, on_delete=models.CASCADE, default=1)
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, default=1)




class PlayList(models.Model):
    list_name = models.CharField(max_length=20)
    build_date = models.DateField()
    list_label = models.CharField(max_length=20)
    list_intro = models.CharField(max_length=30)

    # Relationship set
    user = models.ManyToManyField(AppUser)
    songs = models.ManyToManyField(Song)

