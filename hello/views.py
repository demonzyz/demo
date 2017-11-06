#coding:utf-8
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.contrib import auth

def index(request):
    # data = {'status':'0'}
    # return JsonResponse(data=data)
    return render(request, 'login.html')
    # return HttpResponse('Hello Django')


def findbymonth(request):
    if request.method == 'GET':
        month = request.GET.get('month', None)
        if month is not None:
            bug_info = search_by_month(month)
            # return render(request, 'buginfo.html', {'bug_info':bug_info})
            return JsonResponse(data=bug_info)
        else:
            return HttpResponse(u'缺少参数month', status=400, content_type='text/xml')
    else:
        return HttpResponse(u'该接口只支持GET请求')

@csrf_exempt
def login(request):
    response = ''
    if request.method =='POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if username and password:
            if len(username)>5:
                # if search_user(username, password):
                #     return render(request, 'home.html', {'username':username})
                user = auth.authenticate(username=username, password=password)
                if user:
                    auth.login(request, user)
                    return render(request, 'home.html', {'username': username})
                else:
                    response = u'用户名或密码错误'
            else:
                response = u'username必须大于5位'
        else:
            response = u'缺少必要参数："USERNAME" or "PASSWORD" '
    else:
        response = u'该接口只支持POST请求'
    return render(request, 'error.html', {'info':response})

def search_user(username, password):
    # print os.path.abspath(".")
    try:
        with open(os.path.abspath('.'+'/login.txt')) as f:
            lines = f.readlines()
            for line in lines:
                u = line.split(',')[0].strip()
                p = line.split(',')[1].strip()
                if u == username and p == password:
                    return True
    except:
        return False
    return False


def search_by_month(month):
    data = '''
    {"xAxis":["business_autoFans_J","autoAX","autoAX_admin"],"yAxis":[{"2016_08":[14,7,16],"2016_09":[0,13,12],"2016_10":[24,15,7]},{"2016_08":[0,0,5],"2016_09":[32,31,17],"2016_10":[22,22,9]}, {"2016_08":[0,7,10],"2016_09":[0,0,0],"2016_10":[5,13,2]}]}	
    '''
    show_data = json.loads(data)
    project_name = show_data['xAxis']
    bug_number = []
    for data in show_data['yAxis']:
        sum = 0
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)
        for bug in data['2016_%s' % month]:
            sum += int(bug)
        bug_number.append(sum)
    bug_total = dict(zip(project_name, bug_number))
    return bug_total