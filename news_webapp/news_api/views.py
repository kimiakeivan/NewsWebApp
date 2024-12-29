from django.shortcuts import render
import requests
from datetime import datetime
import pytz
from .models import News
from admin_mode.views import COUNTRIES, CATEGORIES
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.


def home(request):
    news = News.objects.all().order_by('published_at')
    context = {
        'news': news,
        'categories': CATEGORIES,
        'countries': COUNTRIES
    }
    return render(request, 'news_api/home.html', context)





def category_view(request, category):
    news_in_category = News.objects.filter(category=category).order_by('view_count')
    
    context = {
        'news': news_in_category,
        'category': category, 
        'categories': CATEGORIES,
        'countries': COUNTRIES
    }
    print(CATEGORIES)
    print(COUNTRIES)
    return render(request, 'news_api/category.html', context)




def country_view(request, country):
    news_in_category = News.objects.filter(country=country).order_by('view_count')
    
    context = {
        'news': news_in_category,
        'country': country, 
        'countries': COUNTRIES,
        'categories': CATEGORIES,
    }
    return render(request, 'news_api/category.html', context)




@login_required
def foryou(request):
    context = {
    'countries': COUNTRIES,
    'categories': CATEGORIES,
    }
    return render(request, 'news_api/foryou.html', context)




# def home(request):
#     url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
#     response = requests.get(url)
#     data = response.json()

#     articles = data['articles']

#     context = {"articles": articles}

#     return render(request, "news_api/home.html", context)