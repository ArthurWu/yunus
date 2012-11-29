from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404
from models import Article, Menu
    
def article(request, id):
    article = get_object_or_404(Article, pk=id)
    return render(request, 'article.html', {'article': article, 'request': request})