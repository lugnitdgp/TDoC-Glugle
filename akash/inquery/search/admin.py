from django.contrib import admin
from .models import Website
from .crawler import Crawler


@admin.action(description='Start Crawl')
def crawling(modeladmin, request, queryset):
    crawler = Crawler()
    for link in queryset:
        crawler.robot(str(link))
        crawler.crawl(str(link), 1)
    queryset.update(is_crawled=True)


class WebsiteAdmin(admin.ModelAdmin):
    actions = [crawling]

admin.site.register(Website, WebsiteAdmin)
