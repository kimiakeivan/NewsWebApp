from django.db import models

# Create your models here.


class News(models.Model):
    name = models.CharField(null=True,max_length=255)
    author = models.CharField(null=True, max_length=255)
    title = models.CharField(null=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    news_url = models.URLField(null=True, unique=True)
    image_url = models.URLField(blank=True, null=True)
    published_at = models.DateTimeField(null=True)
    content = models.TextField(null=True)
    view_count = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100)
    country = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.category
