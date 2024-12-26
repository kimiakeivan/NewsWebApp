from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news_api.urls')),
    path('', include('admin_mode.urls')),
]
