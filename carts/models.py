# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from products.models import Product
from django.contrib.auth.models import User


class CartManager(models.Manager):
	def new_or_get(self,request):
		cart_id= request.session.get("cart_id",None) #uzmemo broj od trenutnog sessina
		qs=self.get_queryset().filter(id=cart_id)     # filtriramo lookup ako je postoji uzmemo prvi ako ne kreiramo novi i
		if qs.count()==1:  
			new_obj=False                   
			print('cart ID exist')
			cart_obj=qs.first()
			if request.user.is_authenticated() and cart_obj.user is None:
				cart_obj.user=request.user
				cart_obj.save()
		else:
			#cart_obj=cart_create()   # method in viev
			cart_obj=Cart.objects.new(user=request.user)# trough model manager method  
			new_obj=True
			request.session['cart_id']=cart_obj.id
			print(cart_id)
		return cart_obj,new_obj

	def new(self,user=None):
		print(user)
		user_obj=None
		if user is not None:
			if user.is_authenticated:
				user_obj=user
		return self.model.objects.create(user=user_obj)

class Cart(models.Model):
	user        = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
	products	= models.ManyToManyField(Product,blank=True)
	total		= models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
	timestamp	= models.DateTimeField(auto_now_add=True)
	updated		=models.DateTimeField(auto_now=True)

	objects=CartManager()

	def __str__(self):
		return str(self.id)
