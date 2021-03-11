from django.contrib import sitemaps
from django.urls import reverse
from main import views

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['main:home', 'main:base', 'main:about', 'main:info',
                'main:contact',  'main:info', 'main:cookie_policy', 'main:privacy_policy']

    def location(self, item):
        return reverse(item)