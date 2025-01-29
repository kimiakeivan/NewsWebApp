from django.urls import path
from . import views


urlpatterns = [
    # path('update/', views.fetch_and_store_news, name='fetch_and_store_news'),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path('category/<str:category>/',  views.category_view, name='category_view'),
    path('region/<str:country>/', views.country_view, name='country_view'),
    path('foryou/', views.foryou, name='foryou'),
    path('foryou/save_preferences/', views.save_preferences, name='save_preferences'),
    path('signup/', views.signup, name='signup'),
    path('increment_view_count/<int:article_id>/', views.increment_view_count, name='increment_view_count'),
    path('article/<int:news_id>/', views.article_with_no_url, name='article_detail'),
    path('search/', views.search, name='search'),
    path('api/update-news/', views.update_news_api, name='update_news_api'),
    path('api/update-category/<str:category>/', views.update_category_api, name='update_category_api'),

]
