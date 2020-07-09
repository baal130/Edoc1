"""testzs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from newsletter.views import home2, contact, user_detail, user_detail_web,user_detail_extra,user_detail_package,user_detail_worktime
from newsletter.views import user_detail_price,user_detail_social
from testzs.views import about
from bootcamp.core import views as core_views
from dataadd.views import ProfileFollowToggle,ProfileFollowToggleList


from carts.views import cart_home
from django.conf.urls.i18n import i18n_patterns
from search.views import SearchView
#from django.conf.urls.i18n import i18n_patterns
# from sitemap.views import sitemap

# urlpatterns = [
#     url(r'^sitemap\.xml$', sitemap, name='sitemap-xml'),
# ]


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home2, name='home'),# newsletter = ime appa(foldera), view= skripta, home= definirano ime reqesta u def home(request)
    url(r'^contact/$', contact, name='contact'),
    url(r'^about2/$', about, name='about'),
    url(r'^cart/$',cart_home, name='cart'),
    #url(r'^complain/$', 'dataadd.views.complain', name='complain'),
    url(r'^article/', include('dataadd.urls', namespace="dataadd") ),
    url(r'^doctor/', include('newsletter.urls', namespace="newsletter") ),
    url(r'^userdetail/$', user_detail, name='user_details' ),# poziva se u navbar 1 i u viewu od newslettera
    url(r'^userworktime/$', user_detail_worktime, name='user_detail_worktime' ),
    url(r'^userwebsetup/$', user_detail_web, name='user_details_web' ),
    url(r'^userpatientaccepted/$', user_detail_extra, name='user_detail_extra' ),
    url(r'^userserviceprice/$', user_detail_price, name='user_detail_price' ),
    url(r'^userpackage/$', user_detail_package, name='user_detail_package' ),
    url(r'^usersocial/$', user_detail_social, name='user_detail_social' ),

    # url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^profile-follow/$', ProfileFollowToggle.as_view(), name='follow'),
    url(r'^profile-followlist/$', ProfileFollowToggleList.as_view(), name='followlist'),
    #url(r'^test/$', 'dataadd.views.test', name='test' ),
    url(r'^comments/', include('comments.urls', namespace="comments") ),
    url(r'^markdownx/', include('markdownx.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^summernote/', include('django_summernote.urls')),
    #url(r'^friendship/', include('friendship.urls')),
    url(r'^messages/', include('bootcamp.messenger.urls')),
    url(r'^chat/', include('chat.urls', namespace="chat") ),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^(?P<username>[^/]+)/$', core_views.profile, name='profile'),
    url(r'^i18n/', include(('django.conf.urls.i18n','i18n'), namespace='i18n')),
    url(r'^select2/', include('django_select2.urls')),

   # url(r'^i18n/', include('django.conf.urls.i18n')),
    
]

# urlpatterns += i18n_patterns(
    
#     url(r'^news/', include(news_patterns, namespace='news')),
# )

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
