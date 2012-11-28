# encoding: utf-8
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger
from centre.models import Menu, Article, Subscription, HomePicture
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from os import path
import logging
log = logging.getLogger()

from yunus.settings import PROJECT_DIR
UPLOAD_DIR = path.abspath(path.join(PROJECT_DIR, '../upload/'))

TOP_NUMBER = 5

def home(request):
    miniature = Menu.objects.get(name=u"微型企业")
    social = Menu.objects.get(name=u"社会企业")
    about_us = Menu.objects.get(name=u"关于我们")

    miniature_articles = _set_first(miniature.articles.all().order_by('created')[:TOP_NUMBER])
    social_articles = _set_first(social.articles.all().order_by('created')[:TOP_NUMBER])
    about_us_articles = _set_first(about_us.articles.all().order_by('created')[:TOP_NUMBER])
    home_images = HomePicture.objects.all().order_by('order')
    return render(request, 'index.html', locals())

def about_us(request):
    return render(request, 'about_us.html', locals())

def contact_us(request):
    return render(request, 'contact_us.html')

def search(request):
    import datetime
    from django.db.models import Q

    s = datetime.datetime.now()

    q = request.GET.get('q', '')
    results = Article.objects.filter(
        Q(title__contains=q) |
        Q(title_english__contains=q) |
        Q(body__contains=q) |
        Q(body_english__contains=q)
    )

    e = datetime.datetime.now()
    seconds = abs((s-e).total_seconds())
    return render(request, 'search_result.html', locals())

def subscibe(request):
    email = request.GET.get('email', '')
    Subscription(email=email).save()

    return render(request, 'subscibe_success.html', locals())

def _upload(file):
    filepath = UPLOAD_DIR+'\\'+file.name
    attach = open(filepath, 'wb+')
    for chunk in file.chunks():
        attach.write(chunk)
    attach.close()
    return filepath

def send_emails(request):
    import json
    ids = request.POST.get('ids', '')
    objs = Subscription.objects.filter(id__in = json.loads('['+ids.strip(',')+']'))
    if objs:
        subject = request.POST.get('title', '')
        body = request.POST.get('body', '')
        from_email = '175040128@qq.com'
        recipient_list = [i.email for i in objs]
        attachment = request.FILES['attachment']
        file_path = _upload(attachment)

        msg = EmailMessage(subject, body, from_email, recipient_list)
        msg.attach_file(file_path)
        try:
            msg.send()
        except Exception:
            return HttpResponse('邮件发送失败！')
        return HttpResponse('邮件发送成功！')

    return HttpResponse('sended email!')

def change_language(request):
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'

    from django import http
    response = http.HttpResponseRedirect(next)

    lang_code = request.LANGUAGE_CODE
    lang_code = 'en' if lang_code == 'zh-cn' else 'zh-cn'
    if hasattr(request, 'session'):
        request.session['django_language'] = lang_code
    else:
        from django.conf import settings
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)

    log.error('language: '+request.session['django_language'])
    return response

def menu(request, id):
    menu = get_object_or_404(Menu, pk=id)
    sub_menus = Menu.objects.filter(parent__id=id).order_by('order')
    articles_list = Article.objects.filter(menu_id=id)
    if not articles_list and sub_menus:
        articles_list = Article.objects.filter(menu_id=sub_menus[0].id)
    page_num = 10
    articles = _articles_paginator(request, articles_list, page_num)
    return render(request, 'article_list.html', 
        {
            'sub_menus': sub_menus, 
            'menu': menu, 
            'selected_menu_id': sub_menus[0].id if sub_menus else 0,
            'articles': articles,
            'mutilpages': page_num <= len(articles)
        })

def sub_menu(request, id, item_id):
    menu = get_object_or_404(Menu, pk=id)
    sub_menus = Menu.objects.filter(parent__id=id).order_by('order')
    articles_list = Article.objects.filter(menu_id=item_id)
    page_num = 10
    articles = _articles_paginator(request, articles_list, page_num)
    return render(request, 'article_list.html', 
        {
            'sub_menus': sub_menus, 
            'articles': articles, 
            'selected_menu_id': int(item_id),
            'menu': menu,
            'mutilpages': page_num <= len(articles)
        })

@csrf_exempt
def upload_image(request):  
    from settings import MEDIA_DIR, IMAGES_UPLOAD_DIR, MEDIA_URL
    if request.method == 'POST':
        if "upload_file" in request.FILES:  
            f = request.FILES["upload_file"]  
            from PIL import ImageFile, Image
            import os
            from datetime import datetime
            parser = ImageFile.Parser()
            for chunk in f.chunks():  
                parser.feed(chunk)  
            img = parser.close()  

            #在img被保存之前，可以进行图片的各种操作，在各种操作完成后，在进行一次写操作
            dt = datetime.now()
            cur_dir = '%s_%s_%s' % (dt.year, dt.month, dt.day)
            file_path = os.path.join(MEDIA_DIR,IMAGES_UPLOAD_DIR, cur_dir)
            if not os.path.exists(file_path):
                os.mkdir(file_path)

            file_name = '%s_%s_%s' % (dt.hour, dt.minute, dt.second)
            thumb_fn = file_name+'_min'
            f = os.path.join(file_path, file_name)
            tf = os.path.join(file_path, thumb_fn)
            new_img=img.resize((120,120), Image.ANTIALIAS)
            new_img.save(tf+'.jpg','JPEG')
            img.save(f+'.jpg','JPEG')
            return HttpResponse('%s%s/%s/%s.jpg' % (MEDIA_URL, IMAGES_UPLOAD_DIR, cur_dir, file_name))

    return HttpResponse(u"Some error!Upload faild!格式：jpeg")

def _articles_paginator(request, articles_list, page_num):
    paginator = Paginator(articles_list, page_num) # Show 25 articles per page

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)
    return articles

def _set_first(items):
    if items:
        items[0].first = True

    return items