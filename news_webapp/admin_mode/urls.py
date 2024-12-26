from django.urls import path
from . import views


urlpatterns = [
    # path('update/', views.fetch_and_store_news, name='fetch_and_store_news'),
    path('update/', views.fetch_and_store_news, name="fetch_and_store_news"),
    path('addnews/', views.addnews, name="addnews"),
]
