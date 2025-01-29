from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



# Create your models here.


class News(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    author = models.CharField(null=True,blank=True, max_length=255)
    title = models.CharField(null=True,blank=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    news_url = models.URLField(null=True,blank=True, unique=True)
    image_url = models.URLField(blank=True, null=True)
    published_at = models.DateTimeField(null=True, blank=True,)
    content = models.TextField(null=True, blank=True,)
    view_count = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100)
    country = models.CharField(null=True, max_length=100)


    def save(self, *args, **kwargs):
            # ابتدا شیء را ذخیره می‌کنیم تا شناسه (ID) تنظیم شود
            super().save(*args, **kwargs)

            # سپس URL کامل را می‌سازیم
            if not self.news_url:
                # ساخت URL با استفاده از reverse پس از ذخیره‌سازی شیء
                url_path = reverse('article_detail', kwargs={'news_id': self.id})
                self.news_url = f"http://127.0.0.1:8000{url_path}"

                # سپس تغییرات را در پایگاه داده ذخیره می‌کنیم
                super().save(*args, **kwargs)


    def __str__(self):
        return self.category





class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    categories = models.JSONField(blank=True, null=True)  # ذخیره لیست دسته‌بندی‌ها به صورت JSON
    countries = models.JSONField(blank=True, null=True)  # ذخیره کشورهای انتخابی به صورت JSON

    def __str__(self):
        return f"Preferences for {self.user.username}"





class NewsUpdate(models.Model):
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Last updated: {self.last_updated}"