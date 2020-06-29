from django.conf.urls import url
from django.contrib import admin
from . import views
# from .views import (
# 	chat,
# )

app_name = 'chat'
urlpatterns =[
	
	#url(r'$',chat, name='chat'),
	url(r'^ChatPage/$',views.ChatPage, name='chatpage'),
	url(r'^post/$',views.Post, name='post'),
    url(r'^messages/$',views.Messages, name='messages'),
	
]

