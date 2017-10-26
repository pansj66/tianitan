from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from tt_user.models import *
from django.core.mail import send_mail
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_GET,require_http_methods,require_POST
import re
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from celery_tasks import tasks
from utils.decorators import login_required
from itsdangerous import SignatureExpired
# Create your views here.
# /register/


def register(request):
    return render(request, 'tt_user/register.html')


# /user/login/
def login(request):
    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
        checked = 'checked'
    else:
        username = ''
        checked = ''
    return render(request, 'tt_user/login.html', {'username':username, 'checked':checked})


@require_POST
def register_handle(request):
    '''用户的注册处理'''
    # passport = Passport()
    # 上面这段代码出现一个不容易发现的错误, 他会将passport初始化,让register_active视图中的serializer.loads(token.encode())一直是空的
    # 接受数据
    user_name = request.POST.get('user_name')
    pwd = request.POST.get('pwd')
    cpwd= request.POST.get('cpwd')
    email= request.POST.get('email')
    # 判断是否为空
    if not all([user_name, pwd, email]):
        return render(request, 'tt_user/register.html', {'errmsg': '不能为空!'})
    # 判断邮箱是否合法
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'tt_user/register.html', {'errmsg': '邮箱格式不对!'})
    if Passport.objects.filter(username=user_name):
        return redirect(reverse('user:register'))

    passport = Passport.objects.add_passport(username=user_name, password=pwd, email=email)

    serializer = Serializer(settings.SECRET_KEY, 3600)
    token = serializer.dumps({'confirm' : passport.id})
    token = token.decode()
    # print('++++++'+token)
    tasks.send_email.delay(token, user_name, email)


    return redirect(reverse('user:login'))


# 发送邮件练习
# def send(request):
#     msg = '<a href="http://www.baidu.com">点击注册</a>'
#     send_mail('注册激活', '', settings.EMAIL_FROM, ['pan1377161366@163.com'],
#               html_message=msg)
#     return HttpResponse('ok')


@require_GET
def check_user_exist(request):
    '''检测用户是否存在'''
    username = request.GET.get('username')
    print(username)

    try:
        Passport.objects.get(username=username)
        return JsonResponse({'res' : 0})
    except Passport.DoesNotExist:
        return JsonResponse({'res' : 1})


# /user/active/
def register_active(request, token):
    '''注册激活'''
    # print(token)
    serializer = Serializer(settings.SECRET_KEY, 3600)

    try:
        info = serializer.loads(token.encode())

        # print(info,'------->')
        passport_id = info['confirm']
        # print(passport_id)
        # 用户激活
        passport = Passport.objects.get(id=passport_id)
        passport.is_activate = True
        passport.save()
        # 跳转登录页面
        return redirect(reverse('user:login'))
    except SignatureExpired:
        # 返回链接过期
        return HttpResponse('激活链接已经过期')


@require_POST
def login_check(request):
    # 获取数据
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')
    # 判断数据是否为空,all为空返回false
    if not all([username, password, remember]):
        return JsonResponse({'res': 2})

    passport = Passport.objects.get_passport(username=username, password=password)
    if passport:
        # 帐号密码正确
        # 获取当前路径
        # if request.session.has_key('url_path'):

        next_url = request.session.get('url_path', reverse('goods:index'))
        jsr = JsonResponse({'res': 1, 'next_url': next_url})
        if remember == "true":
            #  记住用户名
            jsr.set_cookie('username', username, max_age=7*24*3600)
        else:
            jsr.delete_cookie('username')

        # 记录登录状态
        request.session['islogin'] = True
        request.session['username'] = username
        request.session['passport_id'] = passport.id
        return jsr
    else:
        # 帐号密码不正确
        return JsonResponse({'res':0})


# /user/logout
def logout(request):
    '''退出登陆'''
    request.session.flush()
    return redirect(reverse('user:login'))


@login_required
def user(request):
    '''用户信息页'''
    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_default_address(passport_id=passport_id)
    return render(request, 'tt_user/user_center_info.html', {"page":'user', 'addr':addr})


@login_required
def order(request):
    '''订单详情'''
    return render(request, 'tt_user/user_center_order.html', {'page':'order'})

@require_http_methods(['GET','POST'])
@login_required
def address(request):
    '''收货地址页'''
    # 获取登录用户id
    passport_id = request.session.get('passport_id')
    # 获取默认地址
    addr = Address.objects.get_default_address(passport_id=passport_id)
    return render(request, 'tt_user/user_center_site.html',{'page': 'address', 'addr':addr})


def address_handle(request):
    '''添加用户收货地址'''
    # 接受数据
    recipient_name = request.POST.get('username')
    recipient_addr = request.POST.get('addr')
    recipient_phone = request.POST.get('phone')
    zip_code = request.POST.get('zip_code')

    # 数据校验
    if not all([recipient_name, recipient_addr, recipient_phone, zip_code]):
        # 数据为空返回错误信息
        return  render(request, 'tt_user/user_center_site.html', {'errmsg' : '参数不能为空'})

    # 如果数据能够通过
    passport_id = request.session.get('passport_id')
    Address.objects.add_address(passport_id=passport_id,
                                recipient_phone=recipient_phone,
                                recipient_name=recipient_name,
                                recipient_addr=recipient_addr,
                                zip_code=zip_code)

    return redirect(reverse('user:address'))







































