# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
# from .signals import user_logged_in
from .utils import get_client_city_data, get_client_ip
from django.contrib.auth import user_logged_in,user_logged_out
from django.contrib.auth.models import User
from allauth.account.signals import email_confirmed
from newsletter.models import UserDetails

class UserSessionManager(models.Manager):
    def create_new(self, user, session_key=None, ip_address=None, city_data=None):
        session_new = self.model()
        session_new.user = user
        session_new.session_key = session_key
        if ip_address is not None:
            session_new.ip_address = ip_address
            if city_data:
                session_new.city_data = city_data
                try:
                    city = city_data['city']
                except:
                    city = None
                session_new.city = city
                try:
                    country = city_data['country_name']
                except:
                    country = None
            session_new.country = country
            session_new.save()
            return session_new
        return None
    def delete_session(self,  session_key):
        session_new = self.get(session_key=session_key)
        session_new.delete()
        return None    
class UserSession(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    session_key     = models.CharField(max_length=60, null=True, blank=True)
    ip_address      = models.GenericIPAddressField(null=True, blank=True)
    city_data       = models.TextField(null=True, blank=True)
    city            = models.CharField(max_length=120, null=True, blank=True)
    country         = models.CharField(max_length=120, null=True, blank=True)
    active          = models.BooleanField(default=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    objects = UserSessionManager()

    def __str__(self):
        city = self.city 
        country = self.country
        if city and country:
            return f"{city}, {country}"
        elif city and not country:
            return f"{city}"
        elif country and not city:
            return f"{country}"
        return self.user.username

def user_logged_in_receiver(sender, request,user, *args, **kwargs):
    # mora se napraviti signal u backandu za authentikaciju
    #ili smo uzeli signal iz auth, ali ima extra armgument user instanca, inacse sender bude instanca
    user = user
    # print("nestoposlano")
    ip_address = get_client_ip(request)
    # print(ip_address)
    if(ip_address=='72.14.207.99'): #local
        ip_address='201.175.134.50' # od mexico city adresa
        # ip_address='188.129.62.90' #zagreb  
    
    city_data = get_client_city_data(ip_address) #ne radi na local serveru
    request.session['CITY'] = str(city_data.get('city', 'New York'))
    session_key = request.session.session_key
    UserSession.objects.create_new(
                user=user, 
                session_key=session_key, 
                ip_address=ip_address,
                city_data=city_data
                )
    
    # test=UserSession.objects.delete_session(
                 
    #             session_key=session_key, 
    #             )
    
    
user_logged_in.connect(user_logged_in_receiver)
def user_logged_out_receiver(sender, request,user, *args, **kwargs):
    session_key = request.session.session_key
    try:

        test=UserSession.objects.delete_session(
                 
                session_key=session_key, 
            )
    except:
        pass
user_logged_out.connect(user_logged_out_receiver)

def user_email_confirmed_receiver(request, email_address,*args, **kwargs):
    print("email_confirmed")
    print(email_address)
    print(request.user)
    try:
            
        user_instance=User.objects.filter(email=email_address).first()
        user_detail_instance=UserDetails.objects.get(user=user_instance)
        user_detail_instance.email=email_address
        print(user_detail_instance.email)
        user_detail_instance.save()
    except :
            
        pass
    
    
    
email_confirmed.connect(user_email_confirmed_receiver)

