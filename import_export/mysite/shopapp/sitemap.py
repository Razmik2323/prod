from django.contrib.sitemaps import Sitemap
from .models import Product


class ShopSitemaps(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj: Product):
        return obj.created_at
