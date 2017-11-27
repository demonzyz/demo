# coding=utf-8
from django.shortcuts import render
from rest_framework.decorators import api_view
# Create your views here.
from django.http import HttpResponse, JsonResponse
import json
from api.models import *


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
                Event.objects.create(title=title, address=address, time=time, limit=limit, status=status)
                id = Event.objects.get(title=title).id
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


#添加嘉宾接口
@api_view(['POST', ])
def add_guest(request):
    id = request.POST.get('id', None)
    name = request.POST.get('name', None)
    phone_number = request.POST.get('phone_number', None)
    e_mail = request.POST.get('e_mail', None)
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