# coding=utf-8
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Event(models.Model):
    title = models.CharField(max_length=50, null=False, unique=True)
    limit = models.SmallIntegerField(default=200, null=True)
    status_choice = ((0, '未开始'), (1, '进行中'), (2, '已结束'))
    status = models.SmallIntegerField(choices=status_choice,default=0, null=True)
    address = models.CharField(max_length=50, null=False)
    time = models.DateField(null=False)

    def __unicode__(self):
        return self.title

    class Meta():
        verbose_name = '会议表'
        verbose_name_plural = verbose_name

class Guest(models.Model):
    event = models.ManyToManyField(Event, null=False)
    name = models.CharField(max_length=30, null=False)
    phone_number = models.CharField(max_length=30, null=False)
    e_mail = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return self.name

    class Meta():
        verbose_name = '嘉宾表'
        verbose_name_plural = verbose_name