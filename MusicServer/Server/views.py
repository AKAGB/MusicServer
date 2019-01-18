import json
from datetime import date, datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from Server import models


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


# Create your views here.
def register(request):
    """注册view"""
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        place = request.POST.get('place', '')
        message = '用户名或者密码不正确！'
        if password != password2:
            message = '两次密码输入不一致！'
        else:
            # try:
            user = User.objects.create_user(username=username, password=password)
            reg_time = timezone.now().date()
            appuser = models.AppUser.objects.create(
                user=user, 
                user_name=username, 
                reg_time=reg_time, 
                user_place=place
            )
            auth.login(request, user)
            return HttpResponseRedirect('/index/%s/' % username)
            # except:
            #     message = '用户名已存在或用户名中有不合法字符！'
        return render(request, 'base1.html', {'message': message})
    return render(request, 'base1.html')

@login_required
def index(request, username):
    """主页面view"""
    return render(request, 'query.html', {'username': username})

def login(request):
    """登陆view"""
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        message = '所有字段都必须填写！'
        if username and password:
            username = username.strip()
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/index/%s/' % username)
            else:
                message = '用户名或者密码不正确！'
        return render(request, 'login.html', {'message': message})
    return render(request, 'login.html')

@login_required
def logout(request):
    """注销账户并返回登陆view"""
    auth.logout(request)
    return HttpResponseRedirect('/login/')

@login_required
def getAttr(request):
    func = request.GET.get('func', None)
    attr = request.GET.get('attr', None)
    value = request.GET.get('value', None)
    playlist = request.GET.get('playlist', None)
    username = request.GET.get('username', None)
    attrs = eval('models.%s.getattr()' % func)

    if playlist is not None:
        result = eval('models.%s.getItems(username, attr, value, playlist)' % func)
    else:
        result = eval('models.%s.getItems(username, attr, value)' % func)

    jsondata = {'attrs': attrs, 'result': result, 'table': func}
    
    return JsonResponse(jsondata)

@login_required
def userinfo(request, username):
    appuser = models.AppUser.objects.get(user_name=username)
    # print(appuser)
    result = {
        'username': username,
        'reg_time': appuser.reg_time,
        'user_place': appuser.user_place,
    }
    return render(request, 'userinfo.html', {
        'username': username,
        'result': result,
    })

@login_required
def detail(request, username, table, key):
    """获取单对象详细信息"""
    if table == 'PlayList':
        # 播放列表页面特殊处理
        p = models.PlayList.objects.filter(id=key)
        playlist = p.all().values()[0]
        # 获取歌单所有的歌曲
        songs = list(p[0].songs.all().values())
        # print(songs)
        
        for each in songs:
            # print(each)
            each['singer'] = models.Singer.objects.get(id=each['singer_id']).singer_name
            each['album'] = models.Album.objects.get(id=each['album_id']).album_name

        playlist['build_user'] = p[0].build_user.user_name
        playlist['songs_counts'] = len(songs)
        playlist['songs'] = json.dumps(songs, cls=ComplexEncoder)
        playlist['attrs'] = models.Song.getattr()

        return render(request, 'listDetail.html', {
            'username': username,
            'playlist': playlist,
        })

    else:
        items = {'AppUser': '用户信息', 'Singer': '歌手信息', 'Company': '唱片公司信息',
                    'Album': '专辑信息', 'Song': '歌曲信息'}
        result = eval('models.%s.getItems(username, "id", %s)' % (table, key))[0]
        attrs = eval('models.%s.getDetail()' % table)
        keys = list(result.keys())
        for i in keys:
            # print(i)
            if i not in attrs:
                del result[i]
        return render(request, 'detail.html', {
            'username': username,
            'item': items[table],
            'info_dict': result
        })

@login_required
def playlist(request, username):
    user = models.AppUser.objects.get(user_name=username)
    collect = user.collect_user.all()
    build = user.build_user.all()
    collect_list = list(collect.values())
    build_list = list(build.values())

    for i, each in enumerate(collect):
        collect_list[i]['build_user'] = each.build_user.user_name

    for i, each in enumerate(build):
        build_list[i]['build_user'] = each.build_user.user_name

    attrs = models.PlayList.getattr()
    result = json.dumps(
        {
            'collect_list': collect_list,
            'build_list': build_list,
            'attrs': attrs,
        },
        cls=ComplexEncoder
    )
    return render(request, 'list.html', {
        'username': username,
        'data': result,
    })

@login_required
def createlist(request, username):
    if request.method == 'POST':
        list_name = request.POST.get('list_name', None)
        list_label = request.POST.get('list_label', None)
        list_intro = request.POST.get('list_intro', None)

        pl = models.PlayList.objects.filter(list_name=list_name)
        if len(pl) != 0:
            message = '列表名已存在，请重新输入！'
            return render(request, 'createlist.html', {
                'username': username,
                'message': message,
            })
        
        builder = models.AppUser.objects.get(user_name=username)
        models.PlayList.objects.create(
            list_name=list_name,
            list_label=list_label,
            list_intro=list_intro,
            build_user=builder,
        )

        return HttpResponseRedirect('/index/%s/playlist/' % username)
    return render(request, 'createlist.html', {
        'username': username,
    })

@login_required
def alterPlayList(request):
    username = request.GET.get('username', None)
    playlist = request.GET.get('playlist', None)
    action = request.GET.get('action', None)
    user = models.AppUser.objects.get(user_name=username)
    playlist = models.PlayList.objects.get(list_name=playlist)
        
    if action == '1':
        # 添加联系
        if user not in playlist.user.all():
            playlist.user.add(user)
    else:
        # 删除联系
        if user in playlist.user.all():
            playlist.user.remove(user)

    return JsonResponse({'Action': ('Add' if action=='1' else 'Delete'), 'result': 'Success'})

@login_required
def alterSong(request):
    song_name = request.GET.get('song_name', None)
    list_name = request.GET.get('list_name', None)
    action = request.GET.get('action', None)

    # print(song_name)

    song = models.Song.objects.get(music_name=song_name)
    playlist = models.PlayList.objects.get(list_name=list_name)

    
    if action == '1':
        # 添加联系
        if song not in playlist.songs.all():
            playlist.songs.add(song)
    else:
        # 删除联系
        if song in playlist.songs.all():
            playlist.songs.remove(song)

    return JsonResponse({'Action': ('Add' if action=='1' else 'Delete'), 'result': 'Success'})

@login_required
def getCreateList(request):
    username = request.GET.get('username', None)
    user = models.AppUser.objects.get(user_name=username)
    build = list(user.build_user.all())
    result = [x.list_name for x in build]
    return JsonResponse({'result': result})

