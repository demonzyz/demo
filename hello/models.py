# encoding=utf-8
from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name

    class Meta():
        verbose_name = '作者信息表'
        verbose_name_plural = verbose_name


class Author_Details(models.Model):
    author = models.OneToOneField(Author)
    choice = ((0, '男'), (1, '女'))
    sex = models.SmallIntegerField(choices=choice)
    age = models.SmallIntegerField()
    e_mail = models.CharField(max_length=30, null=True)
    phone_number = models.CharField(max_length=20)


class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=10)
    website = models.CharField(max_length=30)


class Book(models.Model):
    title = models.CharField(max_length=50)
    publication = models.DateField()
    publisher = models.ForeignKey(Publisher)
    author = models.ManyToManyField(Author)
    class Meta():
        verbose_name = '书籍信息表'
        verbose_name_plural = verbose_name



class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=8)