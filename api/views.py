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
#     message = {}
#     if title is  None or address is None or time is None:
#         message = {'error_code': 10001}
#     else:
#         data_title = Add_Event.objects.get(title__iexact=title)
#         try:
#             if Add_Event.objects.filter(title=data_title):
#                 if status not in [0, 1, 2]:
#                     message = {'error_code': 10003}
#                 else:
#                     Add_Event.objects.get_or_create(title=title, address=address, time=time, limit=limit, status=status)
#                     id = Add_Event.objects.get(title=title).id
#                     message = {'error_code': 0, 'data': {'event_id': id, 'statue': 0}}
#         except:
#             message = {'error_code': 10002}
#     return JsonResponse(message)

# @api_view(['POST', ])
def add_event(request):
    title = request.POST.get('title', None)
    address = request.POST.get('address', None)
    time = request.POST.get('time', None)
    limit = request.POST.get('limit', 200)
    status = request.POST.get('status', 0)
    # result = {}
    if title and address and time:
        event = Add_Event.objects.filter(title=title)
        if not event:
            if status in ('0', '1', '2'):
                Add_Event.objects.create(title=title, address=address, time=time, limit=limit, status=status)
                id = Add_Event.objects.get(title).id
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
    result = {}
    if title is not None:
        list = []
        for key in title:
            id = Add_Event.objects.get(title=key).id
            status = Add_Event.objects.get(title=key).status
            list.append({'id': id, 'title': title, 'status': status})
        result = {'event_list': list}
    else:
        result = {'error_code': 10004}
    return JsonResponse(result)