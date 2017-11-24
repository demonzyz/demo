# coding=utf-8
from django.db import models

# Create your models here.


class Add_Event(models.Model):
    title = models.CharField(max_length=50, null=False, unique=True)
    limit = models.SmallIntegerField(default=200, null=True)
    status_choice = ((0, '未开始'), (1, '进行中'), (2, '已结束'))
    status = models.SmallIntegerField(choices=status_choice,default=0, null=True)
    address = models.CharField(max_length=50, null=False)
    time = models.DateField(null=False)


class Add_Guest(models.Model):
    event = models.ForeignKey(Add_Event, null=False)
    name = models.CharField(max_length=30, null=False)
    phone_number = models.CharField(max_length=30, null=False)
    e_mail = models.CharField(max_length=50, null=True)