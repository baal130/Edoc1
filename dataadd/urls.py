from django.conf.urls import url
from django.contrib import admin
from el_pagination.decorators import page_template

from .views import (
	doctor_article_list,
	doctor_article_create,
	doctor_article_detail,
	doctor_article_update,
	doctor_article_delete,
	myarticle,
	article,
	friends,
	connect,
	connectrequest,
	entry_list,
)

app_name = 'dataadd'
urlpatterns =[
	
	#url(r'$',"dataadd.views.complain_create", name='complain'),
	#url(r'$',complain_list, name='complain_list'),
	url(r'connect/(?P<operation>.+)/(?P<pk>\d+)/$',connect,name='connect'),
	url(r'connectrequest/(?P<operation>.+)/(?P<pk>\d+)/$',connectrequest,name='connectrequest'),
	url(r'friends/$',friends,name='friends'),
	url(r'^article/$',article, name='article'),
	url(r'^myarticles/$',myarticle, name='myarticle'),#name ide u html brackete kod hrefa
	url(r'^create/$',doctor_article_create,name='complain'), 
	url(r'^pagin/$',
        page_template('service_list_pag.html')(entry_list), # here is object list 
        {'template': 'test_pag.html'},# here is  called upper  object list template  
        name='pagin'),
	#url(r'^detail/(?P<id>\d+)/$',complain_detail),
	#url(r'^(?P<id>\d+)/$',complain_detail, name='detail'),
	url(r'^(?P<slug>[\w-]+)/$',doctor_article_detail, name='detail'),
	url(r'^(?P<slug>[\w-]+)/edit/$',doctor_article_update, name='update'),
	url(r'^(?P<slug>[\w-]+)/delete/$',doctor_article_delete,name='delete'),
	url(r'$',doctor_article_list, name='complain_list'),
	

	
	
]