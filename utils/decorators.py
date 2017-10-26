# 定义装饰器, 让没有登录的用户访问用户中心的时候,跳转到登陆页面
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


def login_required(view_func):
    def warpper(request, *view_args, **view_kwargs):
        if request.session.has_key('islogin'):
            # 用户已登录
            return view_func(request, *view_args, **view_kwargs)
        else:
            return redirect(reverse('user:login'))
    return warpper