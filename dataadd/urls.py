from django.conf.urls import url
from django.contrib import admin
from el_pagination.decorators import page_template

from .views import (
	complain_list,
	complain_create,
	complain_detail,
	complain_update,
	complain_delete,
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
	url(r'^create/$',complain_create,name='complain'), 
	url(r'^pagin/$',
        page_template('service_list_pag.html')(entry_list), # here is object list 
        {'template': 'test_pag.html'},# here is  called upper  object list template  
        name='pagin'),
	#url(r'^detail/(?P<id>\d+)/$',complain_detail),
	#url(r'^(?P<id>\d+)/$',complain_detail, name='detail'),
	url(r'^(?P<slug>[\w-]+)/$',complain_detail, name='detail'),
	url(r'^(?P<slug>[\w-]+)/edit/$',complain_update, name='update'),
	url(r'^(?P<slug>[\w-]+)/delete/$',complain_delete,name='delete'),
	url(r'$',complain_list, name='complain_list'),
	

	
	
]