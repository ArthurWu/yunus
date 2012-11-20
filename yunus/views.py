# encoding: utf-8
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger
from centre.models import Menu, Article, Subscription

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