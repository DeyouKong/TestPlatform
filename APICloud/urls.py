# -*- coding: utf-8 -*-

# @File: urls
# @Author : "Sampson"
# @Detail :

from django.urls import path
from django.conf.urls import url
from APICloud import views
from TestPlatform.views import index

urlpatterns = [
    url(r'^$', index),
    url(r'^project/', views.project_index),
    url(r'^project_add/', views.project_add),
    url(r'^project_update/', views.project_update),
    url(r'^project_delete/', views.project_delete),

    url(r'^sign/', views.sign_index),
    url(r'^sign_add/', views.sign_add),
    url(r'^sign_update/', views.sign_update),
    url(r'^sign_delete/', views.sign_delete),

    url(r'^env/', views.env_index),
    url(r'^env_add/', views.env_add),
    url(r'^env_update/', views.env_update),

    url(r'^interface_add/', views.interface_add),
    url(r'^interface_update/', views.interface_update),
    url(r'^interface_delete/', views.interface_delete),
    url(r'^interface/', views.interface_index),

    url(r'^case/', views.case_index),
    url(r'^case_add/', views.case_add),
    url(r'^case_run/', views.case_run),

    url(r'^plan/', views.plan_index),
    url(r'^plan_add/', views.plan_add),
    url(r'^plan_run/', views.plan_run),

    url(r'^report/', views.report_index),
    #
    url(r'^findata/', views.findata)

]
