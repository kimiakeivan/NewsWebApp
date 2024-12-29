from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news_api.urls')),
    path('admin/permission/', include('admin_mode.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='news_api/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
