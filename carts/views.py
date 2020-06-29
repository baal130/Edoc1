# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Cart

def cart_create(user=None):
	cart_obj=Cart.objects.create(user=None)
	return cart_obj

def cart_home(request):
	cart_obj, new_obj=Cart.objects.new_or_get(request)
	products=cart_obj.products.all()
	total=0
	for x in products:
		total+=x.price
	print(total)
	cart_obj.total=total
	cart_obj.save()

	# cart_id= request.session.get("cart_id",None) #uzmemo broj od trenutnog sessina ## preseljeno sve u model manager 
	# # if cart_id is None and isinstance(cart_id, int):
	# # 	#print('create new cart')
	# # 	#cart_obj=Cart.objects.create(user=None)
	# # 	cart_obj=cart_create()
	# # 	request.session['cart_id']=cart_obj.id
	# # else:
	# qs=Cart.objects.filter(id=cart_id)     # filtriramo lookup ako je postoji uzmemo prvi ako ne kreiramo novi i
	# if qs.count()==1:                      # dodjelimo broj carta trenutnom sesionu
	# 	print('cart ID exist')
	# 	cart_obj=qs.first()
	# 	if request.user.is_authenticated() and cart_obj.user is None:
	# 		cart_obj.user=request.user
	# 		cart_obj.save()
	# else:
	# 	#cart_obj=cart_create()   # method in viev
	# 	cart_obj=Cart.objects.new(user=request.user)# trough model manager method  
	# 	request.session['cart_id']=cart_obj.id
	# 	print(cart_id)
		
	# #print(request.session)# on the request object
	# #print(dir(request.session))#naredbe sesiona 
	# #key=request.session.session_key
	# #print (key)
	
	# request.session['user']=request.user.username
	return render(request,"carts/home.html",{})
