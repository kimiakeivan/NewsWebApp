from django.urls import path
from . import views


urlpatterns = [
    # path('update/', views.fetch_and_store_news, name='fetch_and_store_news'),
    path('home/', views.home, name='home'),
    path('category/<str:category>/',  views.category_view, name='category_view'),
    path('region/<str:country>/', views.country_view, name='country_view'),
    path('foryou/', views.foryou, name='foryou'),
    path('signup/', views.signup, name='signup'),
]
