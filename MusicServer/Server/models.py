from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20, default='')
    reg_time = models.DateField()
    user_place = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

    @staticmethod
    def getItems(username, attr=None, value=None):
        if attr is None:
            result = AppUser.objects.values()
        else:
            if attr == 'id':
                result = AppUser.objects.filter(id=value).values()
            else:
                result = eval('AppUser.objects.filter(%s__icontains=value).values()' % attr)
        return list(result)

    @staticmethod
    def getDetail():
        return ['user_name','reg_time','user_place']

    @staticmethod
    def getattr():
        return ['user_name','reg_time','user_place']


class Singer(models.Model):
    singer_name = models.CharField(max_length=20)
    singer_en_name = models.CharField(max_length=20)

    def __str__(self):
        return self.singer_name

    @staticmethod
    def getItems(username, attr=None, value=None):
        if attr is None:
            result = Singer.objects.values()
        else:
            if attr == 'id':
                result = Singer.objects.filter(id=value).values()
            else:
                result = eval('Singer.objects.filter(%s__icontains=value).values()' % attr)
        return list(result)

    @staticmethod
    def getDetail():
        return ['singer_name', 'singer_en_name']

    @staticmethod
    def getattr():
        return ['singer_name', 'singer_en_name']

    

class Company(models.Model):
    company_name = models.CharField(max_length=20)
    build_date = models.DateField()
    company_place = models.CharField(max_length=20)
    
    def __str__(self):
        return self.company_name
    
    @staticmethod
    def getDetail():
        return ['company_name','build_date','company_place' ]

    @staticmethod
    def getattr():
        return ['company_name','build_date','company_place' ]

    @staticmethod
    def getItems(username, attr=None, value=None):
        if attr is None:
            result = Company.objects.values()
        else:
            if attr == 'id':
                result = Company.objects.filter(id=value).values()
            else:
                result = eval('Company.objects.filter(%s__icontains=value).values()' % attr)
        return list(result)

class Album(models.Model):
    album_name = models.CharField(max_length=20)
    album_year = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE, default=1)

    outAttrs = {
        'company': ('Company', 'company_name'), 
        'singer': ('Singer', 'singer_name')
    }

    # Relationship set
    users = models.ManyToManyField(AppUser, blank=True)

    def __str__(self):
        return self.album_name
    
    @staticmethod
    def getattr():
        return ['album_name','album_year', 'company', 'singer']

    @staticmethod
    def getDetail():
        return ['album_name','album_year', 'company', 'singer']

    @staticmethod
    def getItems(username, attr=None, value=None):
        if attr is None:
            r = Album.objects.all()
        elif attr in Album.outAttrs:
            ids = eval('%s.objects.filter(%s__icontains=value)' % Album.outAttrs[attr])
            r = eval('Album.objects.filter(%s=ids[0].id)' % attr)
            for each in ids[1:]:
                r |= eval('Album.objects.filter(%s=each.id)' % attr)
        else:
            if attr == 'id':
                r = Album.objects.filter(id=value)
            else:
                r = eval('Album.objects.filter(%s__icontains=value)' % attr)
        result = list(r.values())
        for i, album in enumerate(r):
            result[i]['company'] = album.company.company_name
            result[i]['singer'] = album.singer.singer_name
        return result

class Song(models.Model):
    music_name = models.CharField(max_length=20)
    music_url = models.URLField(default='')
    music_time = models.CharField(max_length=10)
    music_year = models.IntegerField()
    music_style = models.CharField(max_length=10)
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE, default=1)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, default=1)

    outAttrs = {
        'album': ('Album', 'album_name'), 
        'singer': ('Singer', 'singer_name')
    }

    def __str__(self):
        return self.music_name

    @staticmethod
    def getDetail():
        return ['music_name','music_time','music_year',
        'music_style', 'singer', 'album', 'music_url']

    @staticmethod
    def getattr():
        return ['music_name','music_time','music_year',
        'music_style', 'singer', 'album']

    @staticmethod
    def getItems(username, attr=None, value=None, playlist=None):
        if playlist is not None:
            sets = PlayList.objects.get(list_name=playlist).songs.all()
        else:
            sets = Song.objects.all()
        r = sets
        if attr is not None:
            if attr in Song.outAttrs:
                ids = eval('%s.objects.filter(%s__icontains=value)' % Album.outAttrs[attr])
                r = eval('sets.filter(%s=ids[0].id)' % attr)
                for each in ids[1:]:
                    r |= eval('sets.filter(%s=each.id)' % attr)
            else:
                if attr == 'id':
                    r = sets.filter(id=value)
                else:
                    r = eval('sets.filter(%s__icontains=value)' % attr)
        result = list(r.values())
        
        # print('result2', result)

        for i, song in enumerate(r):
            result[i]['singer'] = song.singer.singer_name
            result[i]['album'] = song.album.album_name
        return result

    

class PlayList(models.Model):
    list_name = models.CharField(max_length=20)
    build_date = models.DateField(default=timezone.now)
    list_label = models.CharField(max_length=20)
    list_intro = models.CharField(max_length=30)
    build_user = models.ForeignKey(AppUser, related_name='build_user', on_delete=True, default=1)

    # Relationship set
    user = models.ManyToManyField(AppUser, related_name='collect_user')
    songs = models.ManyToManyField(Song, blank=True)

    def __str__(self):
        return self.list_name

    @ staticmethod
    def getattr():
        return ['list_name','build_date','list_label', 'build_user']
    
    @staticmethod
    def getDetail():
        return ['list_name','build_date','list_label', 'build_user']

    @staticmethod
    def getItems(username, attr=None, value=None, related=False):
        # if not related:
        if attr is None:
            r = PlayList.objects.all()
        else:    
            if attr == 'id':
                r = PlayList.objects.filter(id=value)
            else:
                r = eval('PlayList.objects.filter(%s__icontains=value)' % attr)
        result = list(r.values())
        # print(result)
        for i, playlist in enumerate(r):
            result[i]['build_user'] = playlist.build_user.user_name
            if result[i]['build_user'] == username:
                # 创建者
                result[i]['state'] = 0
            elif len(playlist.user.all().filter(user_name=username)) > 0:
                # 已收藏
                result[i]['state'] = 1
            else:
                # 未收藏
                result[i]['state'] = 2
        
        return result
