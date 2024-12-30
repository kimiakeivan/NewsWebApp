from django.shortcuts import render
import requests
from datetime import datetime
import pytz
from .models import News
from admin_mode.views import COUNTRIES, CATEGORIES
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView


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








class CustomLoginView(LoginView):
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return super().get_success_url()




def signup(request):
    next_url = request.GET.get('next', '/')  # آدرس پیش‌فرض '/'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next_url)  # هدایت به مسیر `next`
    else:
        form = UserCreationForm()
    return render(request, 'news_api/signup.html', {'form': form, 'next': next_url})
