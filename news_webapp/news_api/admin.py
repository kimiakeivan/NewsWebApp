from django.contrib import admin
from .models import News
from .models import NewsUpdate
from .tasks import fetch_and_store_news
from datetime import datetime



# Register your models here.



admin.site.register(News)


@admin.action(description=' update news from api')
def fetch_news(modeladmin, request, queryset):
    print("Fetching news...")
    fetch_and_store_news(request)
    news_update, created = NewsUpdate.objects.get_or_create(id=1)
    news_update.last_updated = datetime.now()
    news_update.save()
    modeladmin.message_user(request, "News successfully fetched and stored")

@admin.register(NewsUpdate)
class NewsUpdateAdmin(admin.ModelAdmin):
    list_display = ('last_updated',) 
    actions = [fetch_news]
