from django.db import models

class Website(models.Model):
    site = models.CharField(max_length=500)
    is_crawled = models.BooleanField(default=False)

    def crawling(modeladmin, request, queryset):
        queryset.update(is_crawled=True)

    def __str__(self):
        return self.site
