from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import pytz
from .models import News
import requests


# Create your views here.

CATEGORIES = ["business", "technology", "sports", "health", "science", "general", "entertainment"]
COUNTRIES = ["iran", "world"]

API_KEY = "d50eed871074413a9bb1f393ede17de6"
BASE_URL = "https://newsapi.org/v2/top-headlines"


def parse_datetime(date_str):
    if date_str:
        # ابتدا تبدیل به زمان UTC
        utc_time = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        
        # تبدیل زمان UTC به زمان محلی
        local_tz = pytz.timezone('Asia/Tehran')  # برای زمان ایران (تهران) تنظیم شده است
        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
        
        return local_time
    return None


def fetch_and_store_news(request):
    for country in COUNTRIES:
        for category in CATEGORIES:
            params = {
                "category": category,
                "apiKey": API_KEY,
            }

            if country == "iran":
                params["country"] = "ir"

            response = requests.get(BASE_URL, params=params)
            
            if response.status_code == 200:
                news_data = response.json().get("articles", [])
                print(f"Articles fetched: {len(news_data)}")

                for item in news_data:
                    if not News.objects.filter(news_url=item.get("url")).exists():
                        News.objects.create(
                            news_url=item.get("url", ""),
                            name=item.get("source", {}).get("name", ""),
                            author=item.get("author", ""),
                            title=item.get("title", ""),
                            description=item.get("description", ""),
                            image_url=item.get("urlToImage", ""),
                            published_at=parse_datetime(item.get("publishedAt")),
                            content=item.get("content", ""),
                            category=category,
                            country=country,
                        )
            else:
                print(f"Error fetching data for country {country} and category {category}: {response.status_code}")


    return JsonResponse({"message": "News successfully fetched and stored"})





