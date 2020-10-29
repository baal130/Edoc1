from django.conf import settings
from django.core.mail import send_mail,EmailMessage,EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
def send_mail_customer(customer_email,products,order_id, phone=None,subject=None ):
	subject=_('Product purchased')
	from_email=settings.DEFAULT_FROM_EMAIL
	to_email= customer_email
	form_message=_('Click link below for visit doctor page.Contact by whatsapp or chat')
	
	template = get_template('email_template_bought_product.html')
	

	context = {
	'subject': subject, 
	'customer_email': customer_email,
	'order_id':order_id,
	
	'products':products,
	'form_message' :form_message, 
	}
	content = template.render(context)
	
	msg = EmailMessage(subject, content, from_email, [to_email,'baal130@gmail.com'])
	msg.content_subtype = 'html'
	
	try:

		msg.send()
	except:
		pass
	
	
	
	return None
def send_mail_product_owner(product_email,customer_email,products,order_id, phone=None,subject=None ):
	subject=_('Product purchased')
	from_email=settings.DEFAULT_FROM_EMAIL
	to_email= product_email
	form_message=_('Your product was bought at TravelDoctor')
	
	template = get_template('email_template_bought_product_to_owner.html')
	

	context = {
	'subject': subject, 
	'customer_email': customer_email,

	'order_id':order_id,
	
	'products':products,
	'form_message' :form_message, 
	}
	content = template.render(context)
	
	msg = EmailMessage(subject, content, from_email, [to_email])
	msg.content_subtype = 'html'
	
	try:

		msg.send()
	except:
		pass
	
	
	
	return None	