# encoding=utf-8
from django.shortcuts import render
import json
from django.contrib import auth
import os
from django.http import HttpResponse,HttpResponseRedirect
from hello.models import *
from django.core.urlresolvers import reverse
# Create your views here.

# def index(request):
#     # print request.path
#     if request.method == 'POST':
#         name = request.POST.get('name', None)
#         if name is not None:
#             info = name
#         else:
#             info = u'缺少name参数'
#     else:
#         info = u'该接口只支持POST请求'
# def index(request):
#     # print request.path
#     print request.get_full_path()
#     if request.method == 'GET':
#         name = request.GET.get('name', None)
#         if name is not None:
#             info = name
#         else:
#             info = u'缺少name参数'
#     else:
#         info = u'该接口只支持get请求'
#     return render(request, 'index.html', {'info': info})

def index(request):

    return render(request, 'index.html')

def findbymonth(request):
    if request.method == 'GET':
        month = request.GET.get('month', None)
        if month is not None:
            bug_info = search_by_month(month)
            return render(request, 'buginfo.html', {'bug_info':bug_info})
        else:
            return HttpResponse('缺少参数month')
    else:
        return HttpResponse(u'该接口只支持GET请求')

def search_by_month(month):
    data='''
{"xAxis":["business_autoFans_J","autoAX","autoAX_admin"],"yAxis":[{"2016_08":[14,7,16],"2016_09":[0,13,12],"2016_10":[24,15,7]},{"2016_08":[0,0,5],"2016_09":[32,31,17],"2016_10":[22,22,9]}, {"2016_08":[0,7,10],"2016_09":[0,0,0],"2016_10":[5,13,2]}]}	
'''
    show_data = json.loads(data)
    project_name = show_data['xAxis']
    bug_number = []
    for data in show_data['yAxis']:
        sum = 0
        if month<10:
            month = '0' + str(month)
        else:
            month = str(month)

        for bug in data['2016_%s' % month]:
            sum += int(bug)
        bug_number.append(sum)

    bug_total = dict(zip(project_name, bug_number))
    print bug_total
    return bug_total

# def login(request):
#     response = ''
#     if request.method == 'POST':
#         username = request.POST.get('username', None)
#         password = request.POST.get('password', None)
#         if username and password:
#             if len(username) > 5:
#                 if checkIn(username, password):
#                     return render(request, 'home.html', {'username':username})
#                 else:
#                     response = u'用户名和密码错误'
#             else:
#                 response = u'username必须大于5位'
#         else:
#             response = u'缺少必要参数：username、password'
#     else:
#         response = u'该接口只支持POST接口请求'
#     return render(request, 'error.html', {'info':response})

def login(request):
    response = ''
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)


        if username and password:
            if len(username) > 3:
                # if checkIn(username, password):
                #     return render(request, 'home.html', {'username':username})
                user = auth.authenticate(username=username, password=password)
                # if user:
                #     auth.login(request, user)
                # user = User.objects.filter(username=username, password=password)
                if user:
                    # return render(request, 'home.html', {'username': username})
                    # reverse('hello.views.home')
                    # return HttpResponseRedirect('/hello/home')
                    request.session['user'] = username
                    return HttpResponseRedirect(reverse('hello.views.home'))
                else:
                    response = u'用户名和密码错误'
            else:
                response = u'username必须大于5位'
        else:
            response = u'缺少必要参数：username、password'
    else:
        response = u'该接口只支持POST接口请求'
    # return render(request, 'error.html', {'info':response})
    # request.session['error_info'] = response
    # return HttpResponseRedirect('/hello/error')
    return HttpResponseRedirect("/hello/error/?error_info=%s" % response)

def checkIn(username,password):
    # print os.path.abspath('.')
    try:
        with open('.\\login.txt', 'r') as f:
            lines =  f.readlines()
            for line in lines:
                u = line.split(',')[0].strip()
                p = line.split(',')[1].strip()
                if u == username and p == password:
                    return True
    except Exception,e:
        print e
        return False
    return False

def home(request):
    return render(request,'home.html', {'username': request.session.get('user', '')})

def error(request):
    # return render(request,'error.html', {'info': request.session.get('error_info', '')})
    error_info = request.GET.get('error_info', None)
    return render(request, 'error.html', {'info': error_info})

def book(request):
    # print Author.objects.get(id=1)

    # print Author.objects.get(name='刘大海')
    # return HttpResponse(Author.objects.get(id=1))
    # return HttpResponse(Author.objects.filter(id=1).query)
    # print Author.objects.get(id=1)
    # print type(Author(name='张三'))
    # print type(Author.objects.create(name='李四'))
    # luxun = Author.objects.get(id=1)
    # Author_Details(sex=0, age=100, phone_number='13800138000', author=luxun).save()
    # tianlaoshi = Author(name='田伟峰')
    # tianlaoshi.save()
    # Author_Details(sex=0, age=30, phone_number='13800138001', author=tianlaoshi).save()
    # Author.objects.all()
    # Author.objects.get(name='鲁迅')
    # Author.objects.filter(name='鲁迅')
    # author = Author.objects.get(id=8)
    # author.name = '天威封'
    # author.save()
    # author = Author.objects.filter(id=8).first()
    # author.name = '天威封2'
    # author.save()
    # author = Author.objects.filter(name__contains='刘').order_by('id')
    # print author
    # author = Author.objects.exclude(name__contains='刘').distinct()
    # print author
    # author = Author.objects.filter(name__contains='杨').values('id')
    # print author
    try:
        if Author.objects.filter(name__exact='刘海'):
            return HttpResponse('134123')
    except:
        return HttpResponse('1')

