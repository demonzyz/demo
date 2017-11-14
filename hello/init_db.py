# coding:utf-8
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")
django.setup()

from hello.models import *
import xlrd
from xlrd import xldate_as_tuple
import sys
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf-8')
print os.path.abspath('.')

book = xlrd.open_workbook(u'../图书信息表.xls')
sheet = book.sheet_by_name(u'作者信息')

for i in range(1,sheet.nrows):
    name = sheet.row_values(i)[0]
    sex = sheet.row_values(i)[1]
    if sex == u'男':
        sex = 0
    else:
        sex = 1
    age = sheet.row_values(i)[2]
    email = sheet.row_values(i)[3]
    phonenumber = str(int(sheet.row_values(i)[4]))

    # author = Author.objects.create(name=name)
    # Author_Details.objects.create(sex=sex, age=age,
    #                                      e_mail=email, phone_number=phonenumber, author=author[0])
    author = Author.objects.get_or_create(name=name)
    Author_Details.objects.get_or_create(sex=sex, age=age,
                          e_mail=email, phone_number=phonenumber, author=author[0])

sheet = book.sheet_by_name(u'出版社信息')
for i in range(1,sheet.nrows):
    name = sheet.row_values(i)[0]
    address = sheet.row_values(i)[1]
    city = sheet.row_values(i)[2]
    website = sheet.row_values(i)[3]
    Publisher.objects.get_or_create(name=name,address=address,city=city,website=website)


sheet = book.sheet_by_name(u'图书信息')
for i in range(1,sheet.nrows):
    title = sheet.row_values(i)[0]
    publication = sheet.row_values(i)[3]
    date = datetime(*xldate_as_tuple(publication, 0))
    publication_date = date.strftime('%Y-%m-%d')
    publisher_name = sheet.row_values(i)[2]
    publisher = Publisher.objects.get(name=publisher_name)
    author_names = sheet.row_values(i)[1].split(',')
    book = Book.objects.get_or_create(title=title, publication=publication_date, publisher=publisher)
    for a in author_names:
        author = Author.objects.get(name=a)
        book[0].author.add(author)



