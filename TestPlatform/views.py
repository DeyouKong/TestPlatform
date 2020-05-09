# -*- coding: utf-8 -*-

# @File: views
# @Author : "Sampson"
# @Detail :

from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import JsonResponse
from django.db.models import Count, F
import json
from django.db import transaction
import logging
from APICloud import forms, models

logger = logging.getLogger(__name__)
collect_logger = logging.getLogger('collect')

def register(request):
    """
    注册函数，使用forms的RegForm
    :param request:
    :return:
    """
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        form_obj = forms.RegForm(request.POST)
        if form_obj.is_valid():
            form_obj.cleaned_data.pop("re_password")
            avatar_img = request.FILES.get("avatar")

            # **kwarg 将字典解开成一个个类似 avatar=avatar_img的形式
            models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar=avatar_img)
            ret["msg"] = "/index/"
            collect_logger.info(form_obj.cleaned_data.get('username') + "注册")
            return JsonResponse(ret)
        else:
            print(form_obj.errors)
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            return JsonResponse(ret)

    # 生成一个 Form 对象
    form_obj = forms.RegForm()
    return render(request, "register.html", {"form_obj": form_obj})


def login(request):
    """
    Sampson:admin1234
    test3:admin1234
    用户登陆
    :param request:
    :return:
    """
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            ret["msg"] = "/index/"
        else:
            ret["status"] = 1
            ret["msg"] = "用户名或密码错误"
        return JsonResponse(ret)

    return render(request, "login.html")


@login_required()
def index(request):
    """
    云测试平台首页
    :param request:
    :return:
    """
    return render(request, "TestPlatform/index.html")


@login_required()
def logout(request):
    """注销"""
    auth.logout(request)
    return redirect("/login/")

@login_required()
def home(request):
    """ 个人中心 """
    return render(request, "404NotFound.html")


@login_required()
def message(request):
    """ 消息中心 """
    return render(request, "404NotFound.html")


@login_required()
def settings(request):
    """ 设置 """
    return render(request, "404NotFound.html")

