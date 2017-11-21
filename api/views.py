# cod
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
import json
from api.models import *


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

# @api_view(['POST', ])
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


def get_eventlist(request):
    title = request.GET.get('title', None)
    data_title = Add_Event.objects.filter(title__contains=title)
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