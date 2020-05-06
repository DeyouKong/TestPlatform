# -*- coding: utf-8 -*-

# @File: sign.py
# @Author : "Sampson"
# @Detail :
# @time : 2020/05/03 22:37


import hashlib

def get_sign(sign_type, data, private_key):
    if sign_type == 1:
        return sign_1(data)
    if sign_type == 2:
        return sign_2(data, private_key)
    if sign_type == 3:
        return sign_3(data)


def sign_1(data):
    return data


def sign_2(data, private_key=''):
    keys = sorted(data.keys())
    temp = ''
    for key in keys:
        temp += data[keys]

    md5 = hashlib.md5()
    temp += private_key
    md5.update(temp.encode(encoding='utf-8'))
    signature = md5.hexdigest()
    data['sign'] = signature
    return data


def sign_3(data):
    keys = sorted(data.keys())
    temp = ''
    for key in keys:
        temp += '"' + key + '"' + ':' + '"' + data[key] + '"' + ','
    temp = '{%s}' % temp[:-1]
    md5 = hashlib.md5()
    md5.update(temp.encode(encoding='utf-8'))
    data['signature'] = md5.hexdigest()
    return data