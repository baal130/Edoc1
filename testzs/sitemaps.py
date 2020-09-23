from django.contrib.sitemaps import Sitemap
from newsletter.models import UserDetails
from django.urls import reverse


class UserDetailsSitemap(Sitemap):
	def items(self):
		return UserDetails.objects.all()

class StaticViewSitemap(Sitemap):
	def items(self):
		return ['termsconditions']
	def location (self,item):
		return reverse(item)
