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
        event = Add_Event.objects.filter(title=title)
        if not event:
            if status in (0, 1, 2):
                Add_Event.objects.create(title=title, address=address, time=time, limit=limit, status=status)
                id = Add_Event.objects.get(title=title).id
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
    data_title = Add_Event.objects.filter(title__contains=title)
    if not data_title:
        result = {'error_code': 10004}
        return HttpResponse(json.dumps(result, ensure_ascii=False))
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
    select_id = Add_Event.objects.filter(id=id)
    if not select_id:
        result = {'error_code': 10004}
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    if select_id:
        title = Add_Event.objects.get(id=id).title
        status = Add_Event.objects.get(id=id).status
        limit = Add_Event.objects.get(id=id).limit
        address = Add_Event.objects.get(id=id).address
        start_time = Add_Event.objects.get(id=id).time.strftime('%Y-%m-%d')
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
    select_id = Add_Event.objects.filter(id=id)
    if not select_id:
        result = {'error_code1': 10004}
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    select_status = Add_Event.objects.get(id=id).status
    if int(set_status) not in (0, 1, 2):
        result = {'error_code': 10004}
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    if select_status is int(set_status):
        result = {'error_code': 10004}
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    if select_id.count() > 0 and select_status is not None:
        set_sql_status = Add_Event.objects.get(id=id)
        set_sql_status.status = set_status
        set_sql_status.save()
        result = {'error_code': 0}
    else:
        result = {'error_code': 10004}
        print '4 select_id is not None and select_status is not None'
    return HttpResponse(json.dumps(result, ensure_ascii=False))