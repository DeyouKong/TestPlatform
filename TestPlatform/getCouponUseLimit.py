# -*- coding: utf-8 -*-

# @File: functions
# @Author : "Sampson"
# @Detail :
# @time : 

import requests
import re
from django.http import JsonResponse
from django.shortcuts import render, redirect



def dbLogin(username="kongdeyou", password="a123456789"):

    """ SQL审核平台登录页，获取csrftoken值 """

    url = "https://dbauto.heyteago.com/authenticate/"
    payload = "username=kongdeyou&password=a123456789"
    header = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "282",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "csrftoken=gsrS66kBVNLoBcgaoAbyKeyyGxa855C3oLUEMP0AGLSIhU3vPu6HDzupnl7HpNYa; sessionid=8zc7mplfx0i3iu84obtb0sang8u6z1cr",
        "Host": "dbauto.heyteago.com",
        "Origin": "https://dbauto.heyteago.com",
        "Referer": "https://dbauto.heyteago.com/sqlquery/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "X-CSRFToken": "gsrS66kBVNLoBcgaoAbyKeyyGxa855C3oLUEMP0AGLSIhU3vPu6HDzupnl7HpNYa",
        "X-Requested-With": "XMLHttpRequest"
    }
    authenticate = requests.request("POST",url, data=payload, headers=header)
    cookie = authenticate.headers["Set-Cookie"]
    csrftoken = re.findall(r'csrftoken=(.+?);', cookie)[0]
    sessionid = re.findall(r'sessionid=(.+?);', cookie)[0]
    return csrftoken,sessionid


def getCouponUseLimit(request):

    """ 查询喜茶券使用限制 """
    if request.method == "POST":
        couponId = request.POST.get("couponId")
        useLimit = request.POST.get("useLimit")
        # categoryLimit = request.POST.get("categoryLimit")
        # productLimit = request.POST.get("productLimit")
        csrftoken, sessionid = dbLogin()
        Cookie = "csrftoken={}; sessionid={}".format(csrftoken, sessionid)

        url = "https://dbauto.heyteago.com/query/"
        header = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "282",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "csrftoken=gsrS66kBVNLoBcgaoAbyKeyyGxa855C3oLUEMP0AGLSIhU3vPu6HDzupnl7HpNYa; sessionid=8zc7mplfx0i3iu84obtb0sang8u6z1cr",
            "Host": "dbauto.heyteago.com",
            "Origin": "https://dbauto.heyteago.com",
            "Referer": "https://dbauto.heyteago.com/sqlquery/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "X-CSRFToken": "gsrS66kBVNLoBcgaoAbyKeyyGxa855C3oLUEMP0AGLSIhU3vPu6HDzupnl7HpNYa",
            "X-Requested-With": "XMLHttpRequest"
        }
        header["Cookie"] = Cookie
        header["X-CSRFToken"] = csrftoken
        payload = ""
        if couponId and useLimit =="1":
            """限定商品"""
            payload = "instance_name=%E5%96%9C%E8%8C%B6go-%E7%94%9F%E4%BA%A7-%E7%81%BE%E5%A4%87&db_name=db_production&schema_name=&tb_name=&sql_content=select+cp.*%2Cp.name+from+coupon_products+cp+left+join+products+p+on+p.id%3Dcp.product_id+where+cp.coupon_id%3D%22{}%22+limit+100%3B&limit_num=100".format(couponId)
        elif couponId and useLimit == "2":
            """限定商品分类"""
            payload = "instance_name=%E5%96%9C%E8%8C%B6go-%E7%94%9F%E4%BA%A7-%E7%81%BE%E5%A4%87&db_name=db_production&schema_name=&tb_name=&sql_content=select+cc.*%2Cc.name+from+coupon_categories+cc+left+join+categories+c+on+c.id%3Dcc.category_id+where+cc.coupon_id%3D%22{}%22+limit+100%3B&limit_num=100".format(couponId)
        res = requests.request("POST", url, data=payload, headers=header).json()
        print(type(res))
        print(res)

        return JsonResponse(res)
    return render(request, "getCouponUseLimit.html")

