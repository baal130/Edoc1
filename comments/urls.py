from django.conf.urls import url
from django.contrib import admin

from .views import (
	
	comment_delete,
	
	
)
app_name = 'comments'

urlpatterns =[
	

	
	url(r'^(?P<id>\d+)/delete/$',comment_delete,name='comment_delete'),
	
	
	
]