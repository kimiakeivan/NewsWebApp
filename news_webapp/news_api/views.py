from django.shortcuts import render
import requests
from datetime import datetime
import pytz
from .models import News, UserPreferences
from .tasks import COUNTRIES, CATEGORIES
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import SignupForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .documents import NewsDocument 
from elasticsearch_dsl.query import MultiMatch 


# Create your views here.

def home(request):
    # news = News.objects.all().order_by('published_at')

    category_news = {}  # a dict to store news of categories
    for category in CATEGORIES: # we need first three news of each category
        news = News.objects.filter(category=category).order_by('-published_at')[:3]  
        category_news[category] = news
        
    # print(category_news)
    # for i,j in category_news.items():
    #     print(i)
    #     print(j)
    context = {
        'category_news': category_news,
        'categories': CATEGORIES,
        'countries': COUNTRIES
    }
    return render(request, 'news_api/home.html', context)




def category_view(request, category):
    news_in_category = News.objects.filter(category=category).order_by('-view_count')
    context = {
        'news': news_in_category,
        'category': category, 
        'categories': CATEGORIES,
        'countries': COUNTRIES
    }
    # print(CATEGORIES)
    # print(COUNTRIES)
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




def article_with_no_url(request, news_id):
    article = get_object_or_404(News, id=news_id)
    context = {
        'article': article,  # استفاده از 'article' به جای 'news'
        'countries': COUNTRIES,
        'categories': CATEGORIES,
    }
    return render(request, 'news_api/article_detail.html', context)  # context به درستی ارسال شود




def increment_view_count(request, article_id):
    article = get_object_or_404(News, id=article_id)

    print(article.id)
    print(article.view_count)
    article.view_count += 1
    print(article.view_count)


    article.save()

    return JsonResponse({'view_count': article.view_count})




@login_required
def foryou(request):

    preferences = UserPreferences.objects.get(user=request.user)
    print(preferences)

    selected_categories = preferences.categories
    selected_countries = preferences.countries
    print(selected_categories)

    category_news = {}
    
    for category in selected_categories:
        news = News.objects.filter(category=category).order_by('-published_at')[:3]
        category_news[category] = news
  
    print(category_news)

    context = {
    'category_news': category_news,
    'countries': COUNTRIES,
    'categories': CATEGORIES,
    }

    return render(request, 'news_api/foryou.html', context)




@login_required
def save_preferences(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            categories = data.get('categories', [])
            preferences, created = UserPreferences.objects.update_or_create(
                user=request.user,
                defaults={'categories': categories}
            )

            category_news = {}
            for category in categories:
                news = News.objects.filter(category=category).order_by('-published_at')[:3]
                category_news[category] = [
                    {
                        'title': article.title,
                        'image_url': article.image_url,
                        'news_url': article.news_url,
                        'published_at': article.published_at,
                        'view_count': article.view_count,
                    }
                    for article in news
                ]

            return JsonResponse({'success': True, 'category_news': category_news})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)




class CustomLoginView(LoginView):
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return super().get_success_url()




def signup(request):
    next_url = request.GET.get('next', '/')  # آدرس پیش‌فرض '/'
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(next_url)  # هدایت به مسیر `next`
    else:
        form = SignupForm()

    return render(request, 'news_api/signup.html', {'form': form, 'next': next_url})




def search(request):

    q = request.GET.get("q")
    if q:
        query = MultiMatch(query=q, fields=["title", "description"], fuzziness="AUTO")
        s = NewsDocument.search().query(query)
        # context['match_articles'] = s

    context = {
        'countries': COUNTRIES,
        'categories': CATEGORIES,
        'match_articles': s,
        'q': q
        }
    return render(request, 'news_api/search.html', context)



def update_news_api(request):
    category_news = {}
    for category in CATEGORIES:
        news = News.objects.filter(category=category).order_by('-published_at')[:3]
        category_news[category] = [
            {
                'id': n.id,
                'title': n.title,
                'news_url': n.news_url,
                'image_url': n.image_url,
                'published_at': n.published_at,
                'view_count': n.view_count
            }
            for n in news
        ]
    
    return JsonResponse({'category_news': category_news})



def update_category_api(request, category):
    news_in_category = News.objects.filter(category=category).order_by('-view_count')
    print(n.published_at)
    news_list = [
        {  
            'title': n.title,
            'name': n.name,
            'id': n.id,
            'description': n.description,
            'content': n.content,
            'news_url': n.news_url,
            'image_url': n.image_url,
            'published_at': n.published_at,
            'view_count': n.view_count,
        }

        for n in news_in_category


    ]
    return JsonResponse({'category': category, 'news': news_list})


