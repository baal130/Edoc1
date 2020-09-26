from django.contrib.sitemaps import Sitemap
from newsletter.models import UserDetails,UserDetailsServicePackagePrice

from django.urls import reverse


class UserDetailsSitemap(Sitemap):
	def items(self):
		return UserDetails.objects.all()
class UserDetailsServicePackagePriceSitemap(Sitemap):
	def items(self):
		return UserDetailsServicePackagePrice.objects.active()
class StaticViewSitemap(Sitemap):
	def items(self):
		return ['termsconditions','privacy']
	def location (self,item):
		return reverse(item)
