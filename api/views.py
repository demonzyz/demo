# coding=utf-8
from django.shortcuts import render
from rest_framework.decorators import api_view
# Create your views here.
from django.http import HttpResponse, JsonResponse
import json
from api.models import *
from rest_framework.authtoken.models import Token
import hashlib
from django.contrib.auth.models import User
import time
from django.db import connection
import base64
from django.contrib import auth


def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

def check_sign(header_dic, query_dic):
    flag = False
    sign = query_dic.get('sign', None)
    username = query_dic.get('username', None)
    token = header_dic.get('HTTP_TOKEN', None)
    random = header_dic.get('HTTP_RANDOM', None)
    md5 = hashlib.md5()
    user = User.objects.filter(username=username)
    if user.exists():
        if token == Token.objects.get(user=user.first()).key and sign:
            if token and len(random) == 5:
                para_str = ''
                if query_dic:
                    list = []
                    for k, v in query_dic.items():
                        if k !='sign' and k !='username':
                            list.append(k + '=' + v)
                    list.sort()
                    para_str = '&'.join(list)
                sign_str = "%spara=%s%s" % (token, para_str, random)
                md5.update(sign_str.encode(encoding="utf-8"))
                server_sign = md5.hexdigest()
                if server_sign == sign:
                    flag = True
    return flag

#登录接口
@api_view(['POST', ])
def register(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    print password
    if username and password:
        password = base64.decodestring(password)[3:]
        user = auth.authenticate(username=username, password=password)
        if user:
            token_str = Token.objects.get(user=user).key
            result = {'error_code': 0, 'token': token_str}
        else:
            result = {'error_code': 10000}
    else:
        result = {'error_code': 10001}
    return JsonResponse(result)


#创建会议接口第一种
# def add_event(request):
#     title = request.POST.get('title', None)
#     address = request.POST.get('address', None)
#     time = request.POST.get('time', None)
#     limit = request.POST.get('limit', 200)
#     status = request.POST.get('status', 0)
#     if title is None or address is None or time is None:
#         message = {'error_code': 10001}
#     else:
#         if Add_Event.objects.filter(title=title):
#             message = {'error_code': 10002}
#         else:
#             if status not in [0, 1, 2]:
#                 message = {'error_code': 10003}
#             else:
#                 Add_Event.objects.get_or_create(title=title, address=address, time=time, limit=limit, status=status)
#                 id = Add_Event.objects.get(title=title).id
#                 message = {'error_code': 0, 'data': {'event_id': id, 'statue': 0}}
#     return JsonResponse(message)


#创建会议接口第二种
@api_view(['POST', ])
def add_event(request):
    title = request.POST.get('title', None)
    address = request.POST.get('address', None)
    time = request.POST.get('time', None)
    limit = request.POST.get('limit', 200)
    status = request.POST.get('status', 0)
    if title and address and time:
        event = Event.objects.filter(title=title)
        if not event:
            if int(status) in (0, 1, 2):
<<<<<<< HEAD
                Event.objects.create(title=title, address=address, time=time, limit=limit, status=status)
                id = Event.objects.get(title=title).id
=======
                Add_Event.objects.get_or_create(title=title, address=address, time=time, limit=limit, status=status)
                id = Add_Event.objects.get(title=title).id
>>>>>>> master
                result = {'error_code': 0, 'data': {'event_id': id, 'statue': 0}}
            else:
                result = {'error_code': 10003}
        else:
            result = {'error_code': 10002}
    else:
        result = {'error_code': 10001}
    return JsonResponse(result)


#查询会议接口第一种
@api_view(['GET', ])
def get_eventlist(request):
    title = request.GET.get('title', None)
    data_title = Event.objects.filter(title__contains=title)
    if not data_title:
        result = {'error_code': 10004}
    if data_title.count() > 0:
        event_list = []
        for key in data_title:
            id = key.id
            status = key.status
            title = key.title
            event_list.append({'id': id, 'title': title, 'status': status})
        result = {'error_code': 0, 'event_list': event_list}
    else:
        result = {'error_code': 10004}
    return HttpResponse(json.dumps(result, ensure_ascii=False))


#查询会议接口第二种
# def get_eventlist(request):
#     title = request.GET.get('title', None)
#
#     if not title:
#         events = Add_Event.objects.all()
#     else:
#         events = Add_Event.objects.filter(title__contains=title)
#     if events.count() > 0:
#         event_list = []
#         for event in events:
#             id = event.id
#             title = event.title
#             status = event.status
#             event_list.append({'id': id, 'title': title, 'status': status})
#         result = {'error_code': 0, 'event_list': event_list}
#     else:
#         result = {'error_code': 10004}
#     # return JsonResponse(result)
#     return HttpResponse(json.dumps(result, ensure_ascii=False))


#查询会议详细信息接口第一种
def get_eventdetail(request):
    id = request.GET.get('id', None)
    select_id = Event.objects.filter(id=id)
    if not select_id:
        result = {'error_code': 10004}
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    if select_id:
        title = Event.objects.get(id=id).title
        status = Event.objects.get(id=id).status
        limit = Event.objects.get(id=id).limit
        address = Event.objects.get(id=id).address
        start_time = Event.objects.get(id=id).time.strftime('%Y-%m-%d')
        result = {'event_detail': {'id': id, 'title': title, 'status': status, 'limit': limit, 'address': address,
                                   'start_time': start_time}, 'error_code': 0}
    else:
        result = {'error_code': 10004}
    return HttpResponse(json.dumps(result, ensure_ascii=False))


#查询会议详细信息接口第二种
# def get_eventdetail(request):
#     id = request.GET.get('id', None)
#     select_id = Add_Event.objects.filter(id=id)
#     if select_id.count() > 0:
#         title = Add_Event.objects.get(id=id).title
#         status = Add_Event.objects.get(id=id).status
#         limit = Add_Event.objects.get(id=id).limit
#         address = Add_Event.objects.get(id=id).address
#         start_time = Add_Event.objects.get(id=id).time.strftime('%Y-%m-%d')
#         result = {'event_detail': {'id': id, 'title': title, 'status': status, 'limit': limit, 'address': address,
#                                    'start_time': start_time}, 'error_code': 0}
#     else:
#         result = {'error_code': 10004}
#     return HttpResponse(json.dumps(result, ensure_ascii=False))


#修改发布会状态接口
@api_view(['POST', ])
def set_status(request):
    id = request.POST.get('id', None)
    set_status = request.POST.get('status', None)
    select_id = Event.objects.filter(id=id)
    if not select_id:
        result = {'error_code': 10004}
        # return HttpResponse(json.dumps(result, ensure_ascii=False))
    select_status = Event.objects.get(id=id).status
    if int(set_status) not in (0, 1, 2):
        result = {'error_code': 10004}
        # return HttpResponse(json.dumps(result, ensure_ascii=False))
    if select_status is int(set_status):
        result = {'error_code': 10004}
        # return HttpResponse(json.dumps(result, ensure_ascii=False))
    if select_id.count() > 0 and select_status is not None:
        set_sql_status = Event.objects.get(id=id)
        set_sql_status.status = set_status
        set_sql_status.save()
        result = {'error_code': 0}
    else:
        result = {'error_code': 10004}
    return HttpResponse(json.dumps(result, ensure_ascii=False))

<<<<<<< HEAD

=======
>>>>>>> master
#添加嘉宾接口
@api_view(['POST', ])
def add_guest(request):
    id = request.POST.get('id', None)
    name = request.POST.get('name', None)
    phone_number = request.POST.get('phone_number', None)
    e_mail = request.POST.get('e_mail', None)
<<<<<<< HEAD
    if id and name and phone_number:
        event = Event.objects.filter(id=id)
        if event.exists():
            count = Guest.objects.filter(event=event.first()).count()
            guest = Guest.objects.filter(phone_number=phone_number)
            if not guest.exists():
                if count < event.first().limit:
                    g = Guest(name=name, phone_number=phone_number, e_mail=e_mail)
                    g.save()
                    g.event.add(event.first())
                    result = {'error_code': 0, "data": {"event_id": id, "guest_id": g.id}}
=======
    # print event_id, '\n', name, '\n', phone_number, '\n', e_mail
    if event_id and name and phone_number:
        id = Add_Event.objects.filter(id=event_id)
        if not id:
            result = {'error_code1': 10004}
            return HttpResponse(json.dumps(result, ensure_ascii=False))
        name_id = Add_Guest.objects.filter(name=name)
        if not name_id:
            status = Add_Event.objects.get(id=event_id).status
            if status is 1:
                limit = Add_Event.objects.get(id=event_id).limit
                if limit < 200:
                    Add_Guest.objects.get_or_create(event_id=event_id, name=name, phone_number=phone_number,e_mail=e_mail)
                    set_sql_limit = Add_Event.objects.get(id=event_id)
                    set_sql_limit.limit += 1
                    set_sql_limit.save()
                    id = Add_Guest.objects.get(name=name).id
                    result = {'error_code': 0, 'data': {'event_id': event_id, 'guest_id': id}}
>>>>>>> master
                else:
                    result = {'error_code': 10006}
            else:
                events_id = guest.first().event.all().values_list('id')
                if (int(id),) not in events_id:
                    if count < event.first().limit:
                        Guest.objects.get(phone_number=phone_number).event.add(event.first())
                        result = {'error_code': 0, "data": {"event_id": id, "guest_id": guest.first().id}}
                    else:
                        result = {'error_code': 10006}
                else:
                    result = {'error_code': 10005}
        else:
            result = {'error_code': 10004}
    else:
        result = {'error_code': 10001}
    return HttpResponse(json.dumps(result, ensure_ascii=False))


#查询嘉宾接口
@api_view(['GET', ])
def get_guestlist(request):
    event_id = request.GET.get('event_id', None)
    phone_number = request.GET.get('phone_number', None)
    if event_id:
        event = Event.objects.filter(id=event_id)
        if event.exists():
            if phone_number:
                guests = Guest.objects.filter(event=event.first(), phone_number=phone_number)
            else:
                guests = Guest.objects.filter(event=event.first())
            if guests.exists():
                guest_list = []
                for guest in guests:
                    guest_info = {}
                    guest_info['guest_id'] = guest.id
                    guest_info['name'] = guest.name
                    guest_info['phone_number'] = guest.phone_number
                    guest_info['e-mail'] = guest.e_mail
                    guest_list.append(guest_info)
                result = {'error_code': 0, 'guest_list': guest_list}
            else:
                result = {'error_code': 10007}
        else:
            result = {'error_code': 10004}
    else:
        result = {'error_code': 10001}
    return HttpResponse(json.dumps(result, ensure_ascii=False))

#嘉宾签到接口
@api_view(['POST', ])
def sign(request):
    event_id = request.POST.get('id', None)
    phone_number = request.POST.get('phone_number', None)
    username = request.POST.get('username', None)
    if event_id and phone_number and username:
        if check_sign(request.META, request.POST):
            event = Event.objects.filter(id=event_id)
            if event.exists():
                n_time = time.time()
                e_time = time.mktime(event.first().time.timetuple())
                if event.first().status != '2' and n_time < e_time:
                    guest = Guest.objects.filter(phone_number=phone_number, event=event.first())
                    if guest.exists():
                        query = "SELECT sign FROM api_guest_event where guest_id=%s and event_id=%s" \
                                %(guest.first().id, event_id)
                        cursor = connection.cursor()
                        cursor.execute(query)
                        is_sign = cursor.fetchone()[0]
                        if is_sign == 0:
                            query = "UPDATE api_guest_event SET sign=1 where guest_id=%s and event_id=%s" \
                                %(guest.first().id, event_id)
                            cursor.execute(query)
                            result = {'error_code': 0}
                        else:
                            result = {'error_code': 10009}
                    else:
                        result = {'error_code': 10008}
                else:
                    result = {'error_code': 10010}
            else:
                result = {'error_code': 10004}
        else:
            result = {'error_code': 10011}
    else:
        result = {'error_code': 10001}
<<<<<<< HEAD
    return JsonResponse(result)
=======
    return HttpResponse(json.dumps(result, ensure_ascii=False))

#查询嘉宾接口
@api_view(['GET', ])
def get_guestlist(request):
    evevt_id = request.GET.get('event_id', None)
    sql_event_id = Add_Guest.objects.filter(event_id=evevt_id)
    if not sql_event_id:
        result = {'error_code': 10007}
    else:
        if sql_event_id.count() > 0:
            guest_list = []
            for key in sql_event_id:
                guest_id = key.id
                guest_name = key.name
                guest_phone_number = key.phone_number
                guest_e_mail = key.e_mail
                guest_list.append({'guest_id': guest_id, 'guest_name': guest_name,
                                   'guest_phone_number': guest_phone_number, 'guest_e_mail': guest_e_mail})
        result = {'guest_list': guest_list, 'error_code': 0}
    return HttpResponse(json.dumps(result, ensure_ascii=False))
>>>>>>> master
