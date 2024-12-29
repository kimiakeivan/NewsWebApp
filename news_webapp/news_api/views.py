from django.shortcuts import render
import requests
from datetime import datetime
import pytz
from .models import News
from admin_mode.views import COUNTRIES, CATEGORIES
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render



# Create your views here.

    # news in homepage
def home(request):
    # news = News.objects.all().order_by('published_at')

    category_news = {}  # a dict to store news of categories
    for category in CATEGORIES: # we need first three news of each category
        news = News.objects.filter(category=category).order_by('-published_at')[:3]  
        category_news[category] = news
        
    # for i,j in category_news.items():
    #     print(i)
    #     print(j)
    context = {
        'category_news': category_news,
        'categories': CATEGORIES,
        'countries': COUNTRIES
    }
    return render(request, 'news_api/home.html', context)




    # news in category
def category_view(request, category):
    news_in_category = News.objects.filter(category=category).order_by('-view_count')
    


    context = {
        'news': news_in_category,
        'category': category, 
        'categories': CATEGORIES,
        'countries': COUNTRIES
    }
    print(CATEGORIES)
    print(COUNTRIES)
    return render(request, 'news_api/category.html', context)




    # iran or world news?
def country_view(request, country):
    news_in_category = News.objects.filter(country=country).order_by('-view_count')
    
    context = {
        'news': news_in_category,
        'country': country, 
        'countries': COUNTRIES,
        'categories': CATEGORIES,
    }
    return render(request, 'news_api/category.html', context)




    #login required! (only if you wish a foryou page)
@login_required
def foryou(request):
    context = {
    'countries': COUNTRIES,
    'categories': CATEGORIES,
    }
    return render(request, 'news_api/foryou.html', context)




