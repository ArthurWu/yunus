# encoding: utf-8
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger
from centre.models import Menu, Article, Subscription
from django.core.mail import EmailMessage
from os import path
import logging
log = logging.getLogger()

from yunus.settings import PROJECT_DIR
UPLOAD_DIR = path.abspath(path.join(PROJECT_DIR, '../upload/'))

TOP_NUMBER = 5

def home(request):
    miniature = Menu.objects.get(name=u"微型企业")
    social = Menu.objects.get(name=u"社会企业")
    #join_us = Menu.objects.get(name=u"加入我们")

    miniature_articles = _set_first(miniature.articles.all().order_by('created')[:TOP_NUMBER])
    social_articles = _set_first(social.articles.all().order_by('created')[:TOP_NUMBER])
    #join_us_articles = _set_first(join_us.articles.all().order_by('created')[:TOP_NUMBER])
    return render(request, 'about_us.html', locals())

def about_us(request):
    return render(request, 'about_us.html', locals())

def contact_us(request):
    return render(request, 'contact_us.html')

def search(request):
    from django.db.models import Q
    q = request.GET.get('q', '')
    results = Article.objects.filter(
        Q(title__contains=q) |
        Q(title_english__contains=q) |
        Q(body__contains=q) |
        Q(body_english__contains=q)
    )
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
    sub_menus = Menu.objects.filter(parent__id=id)
    articles_list = Article.objects.filter(menu_id=id)
    articles = _articles_paginator(request, articles_list)
    return render(request, 'article_list.html', 
        {
            'sub_menus': sub_menus, 
            'menu': menu, 
            'articles': articles
        })

def sub_menu(request, id, item_id):
    menu = get_object_or_404(Menu, pk=id)
    sub_menus = Menu.objects.filter(parent__id=id)
    articles_list = Article.objects.filter(menu_id=item_id)
    articles = _articles_paginator(request, articles_list)
    return render(request, 'article_list.html', 
        {
            'sub_menus': sub_menus, 
            'articles': articles, 
            'selected_menu_id': int(item_id),
            'menu': menu
        })

def _articles_paginator(request, articles_list):
    paginator = Paginator(articles_list, 4) # Show 25 articles per page

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