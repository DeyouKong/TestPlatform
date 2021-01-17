from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from APICloud.models import Project, Sign, Environment, Interface, Case, Plan, Report
from django.core import serializers
from common.execute import Execute
from django.contrib import messages

import time
import json

# Create your views here.

# 项目增删改查
def project_index(request):
    prj_list = Project.objects.all()
    return render(request, "TestPlatform/project/index.html", {"prj_list": prj_list})

def project_add(request):
    if request.method == 'POST':
        prj_name = request.POST['prj_name']
        name_same = Project.objects.filter(name=prj_name)
        if name_same:
            messages.error(request, "项目已存在")
        else:
            description = request.POST['description']
            sign_id = request.POST['sign']
            sign = Sign.objects.get(id=sign_id)
            prj = Project(name=prj_name, description=description, sign=sign)
            prj.save()
            return HttpResponseRedirect("/platform/project/")

    sign_list = Sign.objects.all()
    return render(request, "TestPlatform/project/add.html", {"sign_list": sign_list})

def project_update(request):
    if request.method == 'POST':
        prj_id = request.POST['prj_id']
        prj_name = request.POST['prj_name']
        name_exit = Project.objects.filter(name=prj_name).exclude(id=prj_id)
        if name_exit:
            # messages.error(request, "项目已存在")
            return HttpResponse("项目已存在")
        else:
            description = request.POST['description']
            sign_id = request.POST['sign_id']
            sign = Sign.objects.get(id=sign_id)
            Project.objects.filter(id=prj_id).update(name=prj_name, description=description,sign=sign)
            return redirect("/platform/project/")
    prj_id = request.GET['prj_id']
    prj = Project.objects.get(id=prj_id)
    sign_list = Sign.objects.all()
    return render(request, "TestPlatform/project/update.html", {"prj": prj, "sign_list": sign_list})

def project_delete(request):
    if request.method == 'GET':
        prj_id = request.GET['prj_id']
        Project.objects.filter(id=prj_id).delete()
        return redirect("/platform/project/")


def sign_index(request):
    """ 加密方式增删改查 """
    sign_list = Sign.objects.all()
    return render(request, "TestPlatform/sign/sign_index.html", {"sign_list": sign_list})

def sign_add(request):
    if request.method == 'POST':
        sign_name = request.POST['sign_name']
        description = request.POST['description']
        sign = Sign(name=sign_name, description=description)
        sign.save()
        return HttpResponseRedirect("/platform/sign/")
    return render(request, "TestPlatform/sign/sign_add.html")


def sign_update(request):
    """ 更新加密方式 """
    if request.method == 'POST':
        sign_id = request.POST['sign_id']
        sign_name = request.POST['sign_name']
        description = request.POST['description']
        Sign.objects.filter(id=sign_id).update(name=sign_name, description=description)
        return HttpResponseRedirect("/platform/sign/")
    sign_id = request.GET['sign_id']
    sign = Sign.objects.get(id=sign_id)
    return render(request, "TestPlatform/sign/sign_update.html", {"sign": sign})

def sign_delete(request):
    if request.method == 'GET':
        sign_id = request.GET['sign_id']
        Sign.objects.filter(id=sign_id).delete()
    return redirect("/platform/sign/")


def env_index(request):
    env_list = Environment.objects.all()
    return render(request, "TestPlatform/env/index.html", {"env_list": env_list})


def env_add(request):
    """ 新增测试环境 """
    if request.method == 'POST':
        env_name = request.POST['env_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(id=prj_id)
        url = request.POST['url']
        private_key = request.POST['private_key']
        description = request.POST['description']
        env = Environment(name=env_name, url=url, project=project,
                           private_key=private_key, description=description)
        env.save()
        return HttpResponseRedirect("/platform/env/")
    prj_list = Project.objects.all()
    return render(request, "TestPlatform/env/add.html", {"prj_list": prj_list})

def env_update(request):
    """ 测试环境更新 """
    if request.method == 'POST':
        env_id = int(request.POST['env_id'])
        print(type(env_id))
        env_name = request.POST['env_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(id=prj_id)
        url = request.POST['url']
        private_key = request.POST['private_key']
        description = request.POST['description']
        Environment.objects.filter(id=env_id).update(name=env_name, url=url, project=project, private_key=private_key, description=description)
        return HttpResponseRedirect("/platform/env/")
    env_id = request.GET['env_id']
    env =Environment.objects.get(id=env_id)
    prj_list = Project.objects.all()
    return render(request, "TestPlatform/env/update.html", {"env": env, "prj_list": prj_list})


def env_delete(request):
    ret = {"status": "0", "messages": ""}
    if request.method == 'GET':
        try:
            env_id = request.GET.get('env_id')
            Environment.objects.filter(id=env_id).delete()
            ret["messages"] = "/platform/env_index/"
            return JsonResponse(ret)
        except Exception as err:
            ret["status"] = 1
            ret["messages"] = err
            return ret
    return redirect("")


def interface_index(request):
    if_list = Interface.objects.all()
    return render(request, "TestPlatform/interface/index.html", {"if_list": if_list})


def interface_add(request):
    ret = {"status": "0", "messages": ""}
    if request.method == 'POST':
        if_name = request.POST['if_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(id=prj_id)
        url = request.POST['url']
        method = request.POST['method']
        data_type = request.POST['data_type']
        is_sign = request.POST['is_sign']
        description = request.POST['description']
        request_header_data = request.POST['request_header_data']
        request_body_data = request.POST['request_body_data']
        response_header_data = request.POST['response_header_data']
        response_body_data = request.POST['response_body_data']
        try:
            interface = Interface(name=if_name, url=url, project=project, method=method, data_type=data_type,
                          is_sign=is_sign, description=description, request_header_param=request_header_data,
                          request_body_param=request_body_data, response_header_param=response_header_data,
                          response_body_param=response_body_data)
            interface.save()
        except Exception as err:
            ret["status"] = "1"
            ret["messages"] = err
        return JsonResponse(ret)
    prj_list = Project.objects.all()
    return render(request, "TestPlatform/interface/add.html", {"prj_list": prj_list})

def interface_update(request):
    if request.method == 'POST':
        if_id = request.POST['if_id']
        print(if_id)
        if_name = request.POST['if_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(id=prj_id)
        url = request.POST['url']
        method = request.POST['method']
        data_type = request.POST['data_type']
        is_sign = request.POST['is_sign']
        description = request.POST['description']
        request_header_data = request.POST['request_header_data']
        request_body_data = request.POST['request_body_data']
        response_header_data = request.POST['response_header_data']
        response_body_data = request.POST['response_body_data']
        Interface.objects.filter(id=if_id).update(name=if_name, url=url, project=project, method=method, data_type=data_type,
                          is_sign=is_sign, description=description, request_header_param=request_header_data,
                          request_body_param=request_body_data, response_header_param=response_header_data,
                          response_body_param=response_body_data)
        return HttpResponseRedirect("/platform/interface/")
    if_id = request.GET['if_id']
    prj_list = Project.objects.all()
    if_list = Interface.objects.get(id=if_id)
    return render(request, "TestPlatform/interface/update.html", {"if_list": if_list, "prj_list": prj_list})

def interface_delete(request):
    ret = {"status": "0", "messages": ""}
    print(ret)
    if request.method == 'POST':
        try:
            if_id = request.POST.get('if_id')
            print(if_id)
            Interface.objects.filter(id=if_id).delete()
            ret["messages"] = "/platform/interface/"
            return JsonResponse(ret)
        except Exception as err:
            ret["status"] = 1
            ret["messages"] = err
            return ret
    return redirect("/platform/interface/")

def case_index(request):
    case_list = Case.objects.all()
    env_list = Environment.objects.all()
    return render(request, "TestPlatform/case/index.html", {"case_list": case_list, "env_list": env_list})

def case_add(request):
    if request.method == 'POST':
        case_name = request.POST['case_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(id=prj_id)
        description = request.POST['description']
        content = request.POST['content']
        case = Case(name=case_name, project=project, description=description, content=content)
        case.save()
        return HttpResponseRedirect("/platform/case/")
    prj_list = Project.objects.all()
    return render(request, "TestPlatform/case/add.html", {"prj_list": prj_list})

def case_run(request):
    if request.method == 'POST':
        case_id = request.POST['case_id']
        env_id = request.POST['env_id']
        execute = Execute(case_id, env_id)
        case_result = execute.run_case()
        return JsonResponse(case_result)

def case_delete(request):
    ret = {"status": "0", "messages": ""}
    if request.method == 'POST':
        try:
            case_id = request.POST.get('case_id')
            Case.objects.filter(id=case_id).delete()
            ret["messages"] = "/platform/case_index/"
            return JsonResponse(ret)
        except Exception as err:
            ret["status"] = 1
            ret["messages"] = err
            return ret
    return redirect("/platform/case_index/")


def plan_index(request):
    plan_list = Plan.objects.all()
    return render(request, "TestPlatform/plan/index.html", {"plan_list": plan_list})

def plan_add(request):
    if request.method == 'POST':
        plan_name = request.POST['plan_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(id=prj_id)
        env_id = request.POST['env_id']
        environment = Environment.objects.get(id=int(env_id))
        description = request.POST['description']
        content = request.POST.getlist("case_id")
        plan = Plan(name=plan_name, project=project, environment=environment, description=description, content=content)
        plan.save()
        return HttpResponseRedirect("/platform/plan/")
    prj_list = Project.objects.all()
    env_list = Environment.objects.all()
    return render(request, "TestPlatform/plan/add.html", {"prj_list": prj_list, "env_list": env_list})

def plan_delete(request):
    if request.method == 'GET':
        plan_id = request.GET['plan_id']
        Plan.objects.filter(id=plan_id).delete()
        return redirect("/platform/plan/")

def plan_run(request):
    if request.method == 'POST':
        plan_id = request.POST['plan_id']
        plan = Plan.objects.get(id=plan_id)
        env_id = plan.environment.id
        case_id_list = eval(plan.content)
        case_num = len(case_id_list)
        content = []
        pass_num = 0
        fail_num = 0
        error_num = 0
        for case_id in case_id_list:
            execute = Execute(case_id, env_id)
            case_result = execute.run_case()
            content.append(case_result)
            if case_result["result"] == "pass":
                pass_num += 1
            if case_result["result"] == "fail":
                fail_num += 1
            if case_result["result"] == "error":
                error_num += 1
        report_name = plan.name + "-" + time.strftime("%Y%m%d%H%M%S")
        if Report.objects.filter(plan=plan):
            Report.objects.filter(plan=plan).update(name=report_name, content=content, case_num=case_num,
                                                    pass_num=pass_num, fail_num=fail_num, error_num=error_num)
        else:
            report = Report(plan=plan, name=report_name, content=content, case_num=case_num,
                            pass_num=pass_num, fail_num=fail_num, error_num=error_num)
            report.save()
        return HttpResponse(plan.name + " 执行成功！")

def report_index(request):
    plan_id = request.GET['plan_id']
    report = Report.objects.get(id=plan_id)
    report_content = eval(report.content)
    return render(request, "TestPlatform/report.html", {"report": report, "report_content": report_content})


def findata(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        get_type = request.GET["type"]
        if get_type == "get_all_if_by_prj_id":
            prj_id = request.GET["prj_id"]
            # 返回字典列表
            if_list = Interface.objects.filter(project=prj_id).all().values()
            # list(if_list)将QuerySet转换成list
            return JsonResponse(list(if_list), safe=False)
        if get_type == "get_if_by_if_id":
            if_id = request.GET["if_id"]
            # 查询并将结果转换为json
            interface = Interface.objects.filter(id=if_id).values()
            return JsonResponse(list(interface), safe=False)
        if get_type == "get_env_by_prj_id":
            prj_id = request.GET["prj_id"]
            # 查询并将结果转换为json
            envs = Environment.objects.filter(project_id=prj_id).values()
            return JsonResponse(list(envs), safe=False)
        if get_type == "get_all_case_by_prj_id":
            prj_id = request.GET["prj_id"]
            # 查询并将结果转换为json
            env = Case.objects.filter(project_id=prj_id).values()
            return JsonResponse(list(env), safe=False)