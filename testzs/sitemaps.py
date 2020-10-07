from django.contrib.sitemaps import Sitemap
from newsletter.models import UserDetails,UserDetailsServicePackagePrice
from dataadd.models import Idiot
from products.models import Product
from django.urls import reverse


class UserDetailsSitemap(Sitemap):
	def items(self):
		return UserDetails.objects.all()
class UserDetailsServicePackagePriceSitemap(Sitemap):
	def items(self):
		return UserDetailsServicePackagePrice.objects.active()

class ArticlesSitemap(Sitemap):
	def items(self):
		return Idiot.objects.active()
class ProductsSitemap(Sitemap):
	def items(self):
		return Product.objects.all()

class StaticViewSitemap(Sitemap):
	def items(self):
		return ['termsconditions','privacy',]
	def location (self,item):
		return reverse(item)
