from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone
from Server import models

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
            try:
                user = User.objects.create_user(username=username, password=password)
                reg_time = timezone.now().date()
                appuser = models.AppUser.objects.create(user=user, username=username, reg_time=reg_time, user_place=place)
                auth.login(request, user)
                return HttpResponseRedirect('/index/%s/' % username)
            except:
                message = '用户名已存在！'
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
    print(request.GET)
    func = request.GET.get('func', None)
    attr = request.GET.get('attr', None)
    value = request.GET.get('value', None)
    attrs = eval('models.%s.getattr()' % func)
    if attr is None:
        result = list(eval('models.%s.objects.values()' % func))
    else:
        result = list(eval('models.%s.objects.filter(%s=value).values()' % (func ,attr)))
    jsondata = {'attrs': attrs, 'result': result, 'table': func}
    
    return JsonResponse(jsondata)

@login_required
def userinfo(request, username):
    appuser = models.AppUser.objects.get(user_name=username)
    print(appuser)
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
    items = {'AppUser': '用户信息', 'Singer': '歌手信息', 'Company': '唱片公司信息',
                'Album': '专辑信息', 'Song': '歌曲信息', 'PlayList': '播放列表信息'}
    result = list(eval('models.%s.objects.filter(id=%s).values()' % (table ,key)))[0]
    print(result)
    return render(request, 'detail.html', {
        'username': username,
        'item': items[table],
        'info_dict': result
    })


def playlist(request):
    pass    

