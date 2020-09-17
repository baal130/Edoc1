from django.conf import settings
from django.core.mail import send_mail,EmailMessage,EmailMultiAlternatives

from django.shortcuts import render

from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q,Avg,Count,Max
from django.forms import modelformset_factory,inlineformset_factory

from urllib.parse import quote
from comments.models import Comment
from newsletter.models import SignUp,UserDetails,UserDetailsServicePackagePrice #za query import 
from dataadd.models import Idiot
from newsletter.models import UserDetailsRating,UserDetailsGallery,UserDetailsService,UserDetailsTeam,UserDetailsDepartment,UserDetailsServicePrice
from newsletter.models import UserDetailsLanguage,UserDetailsSocialNetworks,UserDetailsFeatured,UserDetailsServicePackagePriceRemark
from newsletter.forms import ContactForm, SignUpForm,UserDetailsForm,UserWebDetailsForm,UserDetailsGalleryForm,UserDetailsServiceForm
from newsletter.forms import  UserDetailsDepartmentForm,UserDetailsTeamForm,UserDetailsInsuranceForm,PaymentmethodForm,UserDetailsExtraForm,UserDetailsServicePriceForm
from newsletter.forms import	UserDetailsServicePackagePriceForm,UserDetailsLanguageForm,UserDetailsSearchCitiesForm,UserDetailsSearchStateForm
from newsletter.forms import UserDetailsSearchSpecialityForm,UserDetailsSearchServiceForm,UserDetailsFormTime,UserDetailsSocialNetworksForm
from newsletter.forms import AppoitmentForm,ContactDoctorForm,ContactDoctorInListForm,UserDetailsServicePackagePriceRemarkForm
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.shortcuts import render,get_object_or_404, redirect
from testzs.mixins import (
		   
			AjaxRequiredMixin
			)
from django.views.generic import View
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import  NumberInput,HiddenInput,TextInput,Select
import json
import googlemaps
from search.utils import yelp_search,GooglePlaces
from analytics.models import UserSession
import ast
from .languages import categoryYelp
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from allauth.account.models import EmailAddress
from allauth.account.decorators import verified_email_required
from django.contrib.auth.models import User

GOOGLE_CLIENT_API = getattr(settings, 'GOOGLE_CLIENT_API', 'AIzaSyCP-MHkDU5D09akZaDdZF_sCM75KoPpPrI')


class DetailRatingAjaxView(AjaxRequiredMixin, View):
	def post(self,request,*args,**kwargs):
		# print request.POST
		# print("test")
		if not request.user.is_authenticated:
			return JsonResponse({}, status=401)
		user= request.user
		detail_id=request.POST.get("detail_id")
		rating_value_help = request.POST.get("rating_value_help")
		rating_value_kind = request.POST.get("rating_value_kind")
		rating_value_time = request.POST.get("rating_value_time")
		rating_value_staff = request.POST.get("rating_value_staff")
		rating_value_ethic = request.POST.get("rating_value_ethic")
		
		exists=UserDetails.objects.filter(id=detail_id)

		if not exists:

			return JsonResponse({}, status=403)
		try:
			detail_obj=UserDetails.objects.get(id=detail_id)
		except:
			detail_obj=UserDetails.objects.filter(id=detail_id).first()

		rating_obj, rating_obj_created = UserDetailsRating.objects.get_or_create(
				user=user, 
				detail=detail_obj
				)
		try:
			rating_obj = UserDetailsRating.objects.get(user=user, detail=detail_obj)
		except UserDetailsRating.MultipleObjectsReturned:
			rating_obj = UserDetailsRating.objects.filter(user=user, detail=detail_obj).first()
		except:
			#rating_obj = ProductRating.objects.create(user=user, product=product_obj)
			rating_obj = UserDetailsRating()
			rating_obj.user = user
			rating_obj.detail = detail_obj
		if rating_value_help is  not None:
			rating_obj.ratinghelp = int(rating_value_help)
		elif rating_value_kind is not None:   
			rating_obj.ratingkind = int(rating_value_kind)
		elif rating_value_time is not None: 
			rating_obj.ratingtime = int(rating_value_time)
		elif rating_value_staff is not None:     
			rating_obj.ratingstaff = int(rating_value_staff)
		elif rating_value_ethic is not None:     
			rating_obj.ratingethic = int(rating_value_ethic)
		rating_obj.rating = (rating_obj.ratinghelp+rating_obj.ratingkind+ rating_obj.ratingtime+rating_obj.ratingstaff+rating_obj.ratingethic)/5.0
		
		rating_obj.save()

		data = {
			"success": True
		}
		return JsonResponse(data)





# Create your views here.
def home2(request):
	
	package_list=UserDetailsServicePackagePrice.objects.order_by('-packagepricediscount')
	package_list_3=package_list[0:3]
	package_list_6=package_list[3:6]
	package_list_9=package_list[6:9]
	article_list=Idiot.objects.active().filter(article=False)[:3]
	userdetails_contenttype=UserDetails.objects.first().get_content_type

	last_comments=Comment.objects.filter(content_type=userdetails_contenttype).order_by('-id')[:4]
	
	
	queryset_list=UserDetails.objects.filter(
			Q(userdetailsfeatured__rating__gte=0)
		  ).distinct()
	last_6 = queryset_list.order_by('-userdetailsfeatured__rating')[:6]
	verified_user_email=False
	try:
		if EmailAddress.objects.filter(user=request.user, verified=True).exists():
			verified_user_email=True
	except :
		pass
	
	
	context={
		
		"object_list":last_6,
		"article_list":article_list,
		"package_list_3":package_list_3,
		"package_list_6":package_list_6,
		"package_list_9":package_list_9,
		"last_comments":last_comments,
		"verified_user_email":verified_user_email,
	}

		
	
	return render(request,"landing.html",context) #first page
def landingfordoctors(request):
	
	
	context={
		
		
	}

		
	
	return render(request,"landingfordoctors.html",context) #first page
def helpfordoctors(request):
	
	
	context={
		
		
	}

		
	
	return render(request,"landinghelp.html",context) #first page
def contact(request):
	
	title= 'Contact us'
	form=ContactForm(request.POST or None)
	if form.is_valid():
		form_email=form.cleaned_data.get("email")
		form_message=form.cleaned_data.get("message")
		form_full_name=form.cleaned_data.get("full_name")
		
		subject='Site contact form '
		from_email=settings.EMAIL_HOST_USER
		to_email=from_email
		contact_message="%s: %s via %s " %(form_full_name, form_message, form_email)
		send_mail(subject, 
		contact_message, 
			from_email,
			[to_email], 
			fail_silently=False )
		messages.success(request,"Your message has been send",extra_tags='some-tag')#
		return HttpResponseRedirect('/contact')
	
	context={
		"form":form,
		"title":title,
	}           
	return render(request,"contact.html",context)
@verified_email_required
@login_required
def user_detail(request):
	if not request.user.is_authenticated:
		raise Http404
	user_detail_instance=UserDetails.objects.filter(user=request.user) #  instanca od detalja 

	if user_detail_instance.exists():    # means alreday filled once this table  
		user_detail_instance=UserDetails.objects.get(user=request.user)
	
		verificated=False
		title="Your ID is under "
		form= UserDetailsForm( request.POST or None, request.FILES or None,instance=user_detail_instance ) #instance of the form
		
		
		
		
		if form.is_valid(): 
			user_detail_instance=form.save(commit=False)
			user_detail_instance.user=request.user
			user_detail_instance.occupancy="Doctor"
			user_detail_instance.save()
			messages.success(request,_('Your data has been saved'),extra_tags='')#message.tag salje sve tagove(npr sucess + extra tag) i loppa kao charachter stringa
			
				
		if form.errors:
			messages.error(request, _('Sorry,your data has not been saved, please try again'),extra_tags='')
		
			   
		context={
		"form":form,
		"instance":user_detail_instance,
		"verificated":verificated,
		"title":title,
		} 
	else:
		title="Please fill in Your details for verification"
		form= UserDetailsForm( request.POST or None, request.FILES ) #instance of the form

		if form.is_valid(): 
			user_detail_instance=form.save(commit=False)
			user_detail_instance.user=request.user
			
			user_detail_instance.save()

		if form.errors:
			print(form.errors)

		

		context={
		 "form":form,
		
		"title":title,
		} 



	
	return render(request,"user_detail.html",context) 
@login_required	  
def user_detail_worktime(request):
	if not request.user.is_authenticated:
		raise Http404
	user_detail_instance=UserDetails.objects.filter(user=request.user) 

	if user_detail_instance.exists():    
		user_detail_instance=UserDetails.objects.get(user=request.user)
		
		form= UserDetailsFormTime( request.POST or None, request.FILES or None,instance=user_detail_instance ) #instance of the form
		

		if form.is_valid(): 
			user_detail_instance=form.save(commit=False)
			user_detail_instance.user=request.user
			
			user_detail_instance.save()
			messages.success(request,_('Your data has been saved'),extra_tags='')#message.tag salje sve tagove(npr sucess + extra tag) i loppa kao charachter stringa
			
				
		if form.errors:
			messages.error(request, _('Sorry,your data has not been saved, please try again'),extra_tags='')
			   
		context={
		"form":form,
		"instance":user_detail_instance,
		} 
	


	
	return render(request,"user_detail_worktime.html",context) 
@login_required	 
def user_detail_extra(request):
	if not request.user.is_authenticated:
		raise Http404
	user_detail_instance=UserDetails.objects.filter(user=request.user) #  instanca od detalja 
	service_list=UserDetailsService.objects.filter(detail__in=user_detail_instance)
	service_price_list=UserDetailsServicePrice.objects.filter(detail__in=user_detail_instance)
	
	if user_detail_instance.exists():    # means alreday filled once this table  
		user_detail_instance=UserDetails.objects.get(user=request.user)
	
		verificated=False
		title="Your ID is under verification"
		form= UserDetailsExtraForm( request.POST or None, request.FILES or None,instance=user_detail_instance ) #instance of the form
		
		

		if form.is_valid(): 
			user_detail_instance=form.save(commit=False)
			user_detail_instance.user=request.user
			user_detail_instance.save()
			messages.success(request,_('Your data has been saved'),extra_tags='')#message.tag salje sve tagove(npr sucess + extra tag) i loppa kao charachter stringa
			
				
		if form.errors:
			messages.error(request, _('Sorry,your data has not been saved, please try again'),extra_tags='')
			
			   
		context={
		"form":form,
		"service_list":service_list,
		"service_price_list":service_price_list,
		"verificated":verificated,
		"title":title,
		"instance":user_detail_instance,
		
		} 
	else:
		title="Please fill in Your details for verification"
		form= UserDetailsExtraForm( request.POST or None, request.FILES ) #instance of the form

		if form.is_valid(): 
			user_detail_instance=form.save(commit=False)
			user_detail_instance.user=request.user
			print(user_detail_instance.user)
			user_detail_instance.save()

		if form.errors:
			print(form.errors)

		context={
		"form":form,
		"service_list":service_list,
		"service_price_list":service_price_list,
		"title":title,
		} 
	
	return render(request,"user_detail_extra.html",context)
@login_required
def user_detail_price(request):
	if not request.user.is_authenticated:
		raise Http404
	user_detail_instance=UserDetails.objects.filter(user=request.user) #  instanca od detalja 
	service_list=UserDetailsService.objects.filter(detail__in=user_detail_instance)
	service_price_list=UserDetailsServicePrice.objects.filter(detail__in=user_detail_instance)
	# PriceFormset=modelformset_factory(, fields=('name',))
	# formset=PriceFormset(request.POST, queryset=UserDetailsServicePrice.objects.all())
	# for instances in instances: to save formset 

	# PriceFormset=inlineformset_factory(UserDetails,UserDetailsServicePrice, fields=('service','serviceprice','servicepricediscount',)
	# 				,extra=0,can_delete=False,labels={'serviceprice': _('Regular price of service'),'servicepricediscount': _('Discount  on service')},
	# 				widgets=
	# 				{
	# 				'service': Select(attrs={'disabled':'disabled','required':False}),
	# 				'serviceprice': NumberInput(attrs={'placeholder': _('Enter regular price')}),
	# 				'servicepricediscount': NumberInput(attrs={'placeholder': _('Enter discount for regular price in %')}),

	# 				}
	# 				)
	PriceFormset=inlineformset_factory(UserDetails,UserDetailsServicePrice,form=UserDetailsServicePriceForm,extra=0 )


	

	if user_detail_instance.exists():   
		user_detail_instance=UserDetails.objects.get(user=request.user)
		
		verificated=False
		title="Your ID is under verification"
		
		formset=PriceFormset(request.POST or None,instance=user_detail_instance)
		

		
		
		if formset.is_valid():
			
			formset.save()
			formset=PriceFormset( None,instance=user_detail_instance)
			messages.success(request,_('Your data has been saved'),extra_tags='')#message.tag salje sve tagove(npr sucess + extra tag) i loppa kao charachter stringa
			
				
		if formset.errors:
			messages.error(request, _('Sorry,your data has not been saved, please try again'),extra_tags='')	
			   
		context={
		
		"service_list":service_list,
		"service_price_list":service_price_list,
		"verificated":verificated,
		"title":title,
		"formset":formset,
		"instance":user_detail_instance,
		} 
	else:
		title="Please fill in Your details for verification"
		

		

		context={
		
		"service_list":service_list,
		"service_price_list":service_price_list,
		"title":title,
		} 
	
	return render(request,"user_detail_price.html",context)   
@login_required
def user_detail_web(request):
	if not request.user.is_authenticated:
		raise Http404
	user_detail_instance=UserDetails.objects.filter(user=request.user) #  instanca od detalja
	galery_list=UserDetailsGallery.objects.filter(detail__in=user_detail_instance)
	service_list=UserDetailsService.objects.filter(detail__in=user_detail_instance)
	team_list=UserDetailsTeam.objects.filter(detail__in=user_detail_instance)
	department_list=UserDetailsDepartment.objects.filter(detail__in=user_detail_instance)
	language_list=UserDetailsLanguage.objects.filter(detail__in=user_detail_instance)
	
	if user_detail_instance.exists():    # means alreday filled once this table  
		user_detail_instance=UserDetails.objects.get(user=request.user)
		# if user_detail_instance.verificated is  True:        #IF already verificated doesn't need to change anything more
		# 	#print(user_detail_instance.name)
		# 	title="ID verificated"
		# 	verificated=True
			
		# 	context={
		# 	"title":title,
			
		# 	"verificated":verificated,
		# 	}   
		# else:
		verificated=False
		title="Your ID is under verification"
		form= UserWebDetailsForm(  None,  None,instance=user_detail_instance ) #instance of the form
		form2= UserDetailsGalleryForm(  None, None )
		form3=UserDetailsServiceForm(  None, None )
		form4=UserDetailsDepartmentForm(  None, None )
		form5=UserDetailsTeamForm(  None, None )
		form6=UserDetailsInsuranceForm(None, None)
		form7= PaymentmethodForm(None, None)
		form8= UserDetailsLanguageForm(None, None)
		if request.POST.get('Add'): #iz name butona je add
			form2= UserDetailsGalleryForm( request.POST or None, request.FILES or None )
			if form2.is_valid():
				newgallery=UserDetailsGallery()
				newgallery=form2.save(commit=False)
				newgallery.detail=user_detail_instance
				newgallery.save()
				messages.success(request,_('Your data has been saved'),extra_tags='')#message.tag salje sve tagove(npr sucess + extra tag) i loppa kao charachter stringa
				
			else:
				messages.error(request, _('Sorry,your data has not been saved, please try again'),extra_tags='')
		elif request.POST.get('AddService'):
			form3= UserDetailsServiceForm( request.POST or None, request.FILES or None )
			if form3.is_valid():
				newservice=UserDetailsService()
				newservice=form3.save(commit=False)
				newservice.detail=user_detail_instance
				newservice.save()
				print(newservice)
				newpriceservice=UserDetailsServicePrice()
				newpriceservice.detail=user_detail_instance
				newpriceservice.service=newservice
				newpriceservice.save()
				messages.success(request,_('Your data has been saved'),extra_tags='')#message.tag salje sve tagove(npr sucess + extra tag) i loppa kao charachter stringa
				
			else:
				messages.error(request, _('Sorry,your data has not been saved, please try again'),extra_tags='')
			if form3.errors:
				print(form3.errors)    
				
		elif request.POST.get('Add department'):
			form4= UserDetailsDepartmentForm( request.POST or None, request.FILES or None )
			if form4.is_valid():
				newdepartment=UserDetailsDepartment()
				newdepartment=form4.save(commit=False)
				newdepartment.detail=user_detail_instance
				newdepartment.save()
				messages.success(request,_('Your data has been saved'),extra_tags='')#message.tag salje sve tagove(npr sucess + extra tag) i loppa kao charachter stringa
				
			else:
				messages.error(request, _('Sorry,your data has not been saved, please try again'),extra_tags='')
		elif request.POST.get('Add member'):
			form5= UserDetailsTeamForm( request.POST or None, request.FILES or None )
			if form5.is_valid():
				newmember=UserDetailsTeam()
				newmember=form5.save(commit=False)
				newmember.detail=user_detail_instance
				newmember.save()
				messages.success(request,_('Your data has been saved'),extra_tags='')#message.tag salje sve tagove(npr sucess + extra tag) i loppa kao charachter stringa
				
			else:
				messages.error(request, _('Sorry,your data has not been saved, please try again'),extra_tags='')        
		elif request.POST.get('Add Insurance'):
			# print(user_detail_instance.insurancecompany.all())
			# print("nest")
			# user_detail_instance.insurancecompany.clear()
			form6= UserDetailsInsuranceForm( request.POST or None, request.FILES or None,instance=user_detail_instance )
			if form6.is_valid():
				
				form6.save()
				messages.success(request,_('Your data has been saved'),extra_tags='')#message.tag salje sve tagove(npr sucess + extra tag) i loppa kao charachter stringa
				
			else:
				messages.error(request, _('Sorry,your data has not been saved, please try again'),extra_tags='')
		elif request.POST.get('Add Payment'):
			form7= PaymentmethodForm( request.POST or None, request.FILES or None,instance=user_detail_instance )
			if form7.is_valid():		
				form7.save()
				messages.success(request,_('Your data has been saved'),extra_tags='')#message.tag salje sve tagove(npr sucess + extra tag) i loppa kao charachter stringa
				
			else:
				messages.error(request, _('Sorry,your data has not been saved, please try again'),extra_tags='')
		elif request.POST.get('Add Language'):
			form8= UserDetailsLanguageForm( request.POST or None, request.FILES or None )
			if form8.is_valid():		
				
				newlang=UserDetailsLanguage()
				newlang=form8.save(commit=False)
				newlang.detail=user_detail_instance
				newlang.save()
				messages.success(request,_('Your data has been saved'),extra_tags='')#message.tag salje sve tagove(npr sucess + extra tag) i loppa kao charachter stringa
				
			else:
				messages.error(request, _('Sorry,your data has not been saved, please try again'),extra_tags='')			
		else:

			form= UserWebDetailsForm( request.POST or None, request.FILES or None,instance=user_detail_instance ) #instance of the form
			
			if form.is_valid(): 
				user_detail_instance=form.save(commit=False)
				user_detail_instance.user=request.user
				print(user_detail_instance)
				user_detail_instance.save()
				messages.success(request,_('Your data has been saved'),extra_tags='')#message.tag salje sve tagove(npr sucess + extra tag) i loppa kao charachter stringa
			if form.errors:
				messages.error(request, _('Sorry,your data has not been saved, please try again'),extra_tags='')	
			
				
				
			
				
		context={
		"form":form,
		"form2":form2,
		"form3":form3,
		"form4":form4,
		"form5":form5,
		"form6":form6,
		"form7":form7,
		"form8":form8,
		"verificated":verificated,
		"title":title,
		"galery_list":galery_list,
		"service_list":service_list,
		"team_list":team_list,
		"department_list":department_list,
		"language_list":language_list,
		"instance":user_detail_instance,
			} 
	else:
		title="Please fill in Your details for verification"
		form= UserWebDetailsForm( request.POST or None, request.FILES ) #instance of the form

		if form.is_valid(): 
			user_detail_instance=form.save(commit=False)
			user_detail_instance.user=request.user
			
			user_detail_instance.save()

		if form2.errors:
			print(form2.errors)

		 
		context={
		 "form":form,
		
		"title":title,
		} 



	
	return render(request,"user_detail_web.html",context) 


def doctor_list(request): #list items
	#queryset_list=Idiot.objects.filter(draft=False).filter(publish__lte=timezone.now())#all()  #lte means l then or equal pusblish is model field ovo se koristi normalno
	title=''
	city_form=UserDetailsSearchCitiesForm(request.GET or None)
	state_form=UserDetailsSearchStateForm(request.GET or None)
	speciality_form=UserDetailsSearchSpecialityForm(request.GET or None)
	service_form=UserDetailsSearchServiceForm(request.GET or None)
	contact_form=ContactDoctorInListForm(request.GET or None)
	# queryset_list=UserDetails.objects.active().filter(article=False)   #filter je napravljen u modelima i instaciran 
	queryset_list=UserDetails.objects.all()
	test=UserDetails.objects.all()
	
	# print(test)
	# print(test.user.userdetailsrating)
	# user ima one to one prema userdetailrs rating a test ima usera
	
	# if  request.user.is_staff or request.user.is_superuser: 
	#     queryset_list=UserDetails.objects.all()
	query=request.GET.get("q")
	state=request.GET.get("state")# ime state ce bit iz forma fielda
	city=request.GET.get("city")
	speciality=request.GET.get("speciality")
	service=request.GET.get("service")
	lat=latgetexist=request.GET.get('lat')
	lng=request.GET.get('lng')

	#############################################################
	## If search trough "search here feature " query from todos doctors will try to find trough clicked state
	if lat and not state:	
		gmaps = googlemaps.Client(key='AIzaSyAqOazqPcP8E-_s-Vp7MRbP3UMUgS2xfQw')
		LatLng=lat, lng	
		geocode_result = gmaps.reverse_geocode(LatLng)
		
		components=geocode_result[0]['address_components']
		for comp in components:
			for type in comp['types']:
				if type == 'administrative_area_level_1':
					print(comp['long_name'])   #vratit ce drzavu u meksiku 
					state=comp['long_name']
############################### query ################################
	if query:
		
		queryset_list=queryset_list.filter(
			Q(name__icontains=query)|
			Q(surname__icontains=query)
			 
			#Q(user__last_name__icontains=query)
				).distinct()
	if(state):
		
		queryset_list=queryset_list.filter(
			Q(state__icontains=state)
		  ).distinct()
	if(city):
		
		queryset_list=queryset_list.filter(
			Q(city__icontains=city)
		  ).distinct()
	# else: # ako se ništa ne definira napravi search na user sessionu inace stavi sve nadjeno
	# 	if not service  and not speciality and not state and not query:
	# 		citysession = request.session.get('CITY', 'Newport Beach')
	# 		queryset_list=queryset_list.filter(
	# 		Q(city__icontains=citysession)
	# 	  ).distinct()

	if(speciality):
		
		queryset_list=queryset_list.filter(
			Q(speciality__icontains=speciality)
		  ).distinct()      	
	if(service):
		
		
		queryset_list=queryset_list.filter(
			Q(userdetailsservice__servicename__icontains=service)
		  ).distinct()			
	if any((query,state,city,speciality,service,lat)):
		title=_('Search results')
	else:
		queryset_list=queryset_list.filter(
			Q(userdetailsfeatured__rating__gte=0)
		  ).distinct()
		title=_('Featured Doctors')
	# print(queryset_list.first().profilepicture.url)
	paginator = Paginator(queryset_list, 4) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	
	
#################################################################################################
# handles separate search for google and yelp 
#
################################################################################################	

	loc =city
	try:
		#ako ima usera uzmi njegov grad
		user_session_instance=UserSession.objects.filter(user=request.user).first()
		city_data=user_session_instance.city_data
		city_data_decoded = ast.literal_eval(city_data)
	except:
		pass
	
	
	#---lat,lng za search u funkcijama yelp i google
	# ako nije zadana lat,lng uzme se od prvog resultata ili od user sessiana 
	if not lat:
		try:# uzmi od prvog nadjenog na todosdoctors
			lat=queryset_list.first().lat
			lng=queryset_list.first().lng
		except:
			try:
			#  od user sessiana
				lat=city_data_decoded['latitude']
				lng=city_data_decoded['longitude']
			except:
				#od mexica city 
				lat=19.39068
				lng=-99.2836985

	else:   
		pass
	if city:
		# napraviti tablicu za meksicke gradove da se ne koristi preko google maps
		# ako je odabran city u yelo i google funkcije idu koordinate od grada
		try:
			gmaps = googlemaps.Client(key='AIzaSyAqOazqPcP8E-_s-Vp7MRbP3UMUgS2xfQw')	
			geocode_result = gmaps.geocode(city)
		
			lat=geocode_result[0]['geometry']['location']['lat']
			lng=geocode_result[0]['geometry']['location']['lng']
		except:
			pass

	key='doctor'
	if not loc:
		location = request.session.get('CITY', 'Newport Beach')
		# print(location)
	else:
		location = loc
	# categories treba napravit pres speciality
	if (speciality):
		try:
			categories=categoryYelp[speciality]
		except:
			categories='doctor'
	else:
		categories='doctor'
		
	items={'businesses':[]}	
	if any((query,state,city,speciality,service,latgetexist)):
		
		try:
			items = yelp_search(keyword=key, location=location,lat=lat,lng=lng,categories=categories)
			
		except:
			items={'businesses':[]}	
		# for biz in items['businesses']:
		# 	print(biz['location'])
	

	if (items['businesses']):
		resultsYelpExist="true" # true je za javascript koji se salje tamo
		# salje koordinate u ulurusearch jer tamo nemoze proc debug ako je varijabla prazna
		#lathtml is used for coordinate where google map is centered
		lathtml=items['businesses'][0]['coordinates']['latitude']
		lnghtml=items['businesses'][0]['coordinates']['longitude']
	else:
		resultsYelpExist="false"
		lathtml=lat
		lnghtml=lng
	
	api = GooglePlaces(GOOGLE_CLIENT_API)
	coordinate=19.040034,-98.2630055
	coordinate="{0},{1}".format(lat,lng)

	placesgoogle={'results':[]}
	if any((query,state,city,speciality,service,latgetexist)):
		
		#make search in google only when result is filtered
		if speciality:
			keywordgoogle=speciality
			distance=10000
		else:
			keywordgoogle='doctor'
			distance=10000
		print("coordinate")
		print(coordinate)
		placesgoogle = api.search_places_by_coordinate(coordinate, distance, "doctor",keywordgoogle)	
		try:
			placesgoogle = api.search_places_by_coordinate(coordinate, distance, "doctor",keywordgoogle)
			

		except:
			placesgoogle={'results':[]}
		# print(placesgoogle)
		if(placesgoogle['results']):
			print("imagoogle")
		else:
			print("nemagoogle")
		fields = [ 'international_phone_number', 'website',]
		# samo telefon bi trebalo izvuc iz detailss(placa se)
		
		listplaces=[]
		for place in placesgoogle['results']:
			# place is dictionary 
			details = api.get_place_details(place['place_id'], fields)
			
			try:
				result=details['result']
				listplaces.append(result.copy()) #dodaje dictionary na listu (ne treba)
				place.update(result)  #dodaje  u placesgoogle cijeli dictionary	
			except:
				pass	
			
		listgoogle=placesgoogle['results']
		placesgoogle['results']=sorted(placesgoogle['results'], key = lambda i: (i['rating'],i['user_ratings_total']),reverse=True)

	if not (placesgoogle['results']) and not (items['businesses']):
		otherresults=False
	else:
		otherresults=True	
	context={
		"object_list":queryset,
		"title":title,
		"page_request_var":page_request_var,
		"state_form":state_form,
		"city_form":city_form,
		"speciality_form":speciality_form,
		"service_form":service_form,
		"contact_form":contact_form,
		"results":items,
		"placesgoogle":placesgoogle,
		"lathtml":lathtml,
		"lnghtml":lnghtml,
		"otherresults":otherresults,

	}      
	
	return render(request,"doctor_list.html",context)
def discount_list(request,template=None, extra_context=None): 
	city_form=UserDetailsSearchCitiesForm(request.GET or None)
	service_form=UserDetailsSearchCitiesForm(request.GET or None)
	state_form=UserDetailsSearchStateForm(request.GET or None)
	speciality_form=UserDetailsSearchSpecialityForm(request.GET or None)
	service_form=UserDetailsSearchServiceForm(request.GET or None)
	
	
	queryset_list=UserDetailsServicePackagePrice.objects.filter(offerstarts__lte=timezone.now()).filter(offerends__gt=timezone.now())
	queryset_list=queryset_list.order_by('-packagepricediscount')
	# test=queryset_list.first().offerends-timezone.now()# timedate.delta
	
	
	# print('Type :- ',type(test))
	
	query=request.GET.get("q")
	state=request.GET.get("state")# ime state ce bit iz forma fielda
	city=request.GET.get("city")
	speciality=request.GET.get("speciality")
	service=request.GET.get("service")
	
	
	
	if query:
		

		queryset_list=queryset_list.filter(
			Q(service__icontains=query)|
			Q(detail__name__icontains=query)|
			Q(detail__surname__icontains=query)|
			Q(detail__state__icontains=query)|
			Q(detail__city__icontains=query)|
			Q(detail__speciality__icontains=query)|
			Q(headdescription__icontains=query)| 
			Q(description__icontains=query)|
			Q(extragift__icontains=query)

			#Q(user__last_name__icontains=query)
				).distinct()
	if(state):
		
		queryset_list=queryset_list.filter(
			Q(detail__state__icontains=state)
		  ).distinct()
	if(city):
		
		queryset_list=queryset_list.filter(
			Q(detail__city__icontains=city)
		  ).distinct()

	if(speciality):
		
		queryset_list=queryset_list.filter(
			Q(detail__speciality__icontains=speciality)
		  ).distinct()      	
	if(service):
		
		novalist=service.split() #json dump dodaje znakove pa je sevice lista u textu i nemoze se dobro pretraziviati
								 #pa se pretrazuje rijec po rijec
		
		q_objects = Q() # Create an empty Q object to start with
		for t in novalist:
			q_objects |= Q(service__icontains=t) # 'or' the Q objects together


		queryset_list=queryset_list.filter(
				q_objects
			
					
		  ).distinct()			
	if any((query,state,city,speciality,service)):
		title=_('Search results')
	else:
		
		title=_('Top Offers')
	# print(queryset_list.first().profilepicture.url)
	paginator = Paginator(queryset_list, 4) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	
	
	
	context={
		"package_list":queryset,
		"title":title,
		"page_request_var":page_request_var,
		"state_form":state_form,
		"city_form":city_form,
		"speciality_form":speciality_form,
		"service_form":service_form,
		
		

	}      
	return render(request,template,context) 	
@login_required
def delete_galery(request,pk):
	to_delete=UserDetailsGallery.objects.get(pk=pk)
	  
	to_delete.delete()  
	return redirect('/userwebsetup/')
@login_required
def delete_service(request,pk):
	to_delete=UserDetailsService.objects.get(pk=pk)
	  
	to_delete.delete()  
	return redirect('/userwebsetup/')
@login_required
def delete_team(request,pk):
	to_delete=UserDetailsTeam.objects.get(pk=pk)
	print(to_delete)  
	to_delete.delete()  
	return redirect('/userwebsetup/')
@login_required
def delete_department(request,pk):
	to_delete=UserDetailsDepartment.objects.get(pk=pk)
	print(to_delete)  
	to_delete.delete()  
	return redirect('/userwebsetup/')
@login_required
def package_delete(request,pk):
	to_delete=UserDetailsServicePackagePrice.objects.get(pk=pk) 
	to_delete.delete()  
	return redirect('/userwebsetup/')	  
@login_required
def language_delete(request,pk):
	to_delete=UserDetailsLanguage.objects.get(pk=pk) 
	to_delete.delete()  
	return redirect('/userwebsetup/')	

def entry_list(request, slug,template=None, extra_context=None): #retrieve
	
	instance=get_object_or_404(UserDetails,slug=slug) 
	article_list=instance.user.idiot_set.all()
	rating_obj= UserDetailsRating.objects.filter(user=instance.user,detail=instance)
	rating_avg =instance.userdetailsrating_set.aggregate(Avg("rating"),Count("rating"))# rating_avg je object
	#od instanca(doctor detail smo uzeli reverse relatnship i racunamo od svih korisnika average) foreign key u UserdetailsRating
	
	if rating_avg["rating__avg"] is not None:
		rating_avg_int =int(rating_avg["rating__avg"])#dictionary 
	else:
		rating_avg_int=5
	
	

	galery_list=UserDetailsGallery.objects.filter(detail=instance)
	service_list_6=UserDetailsService.objects.filter(detail=instance)[:6]
	service_list_all=UserDetailsService.objects.filter(detail=instance)
	team_list=UserDetailsTeam.objects.filter(detail=instance)
	department_list=UserDetailsDepartment.objects.filter(detail=instance)
	insurance_list=instance.insurancecompany.all()
	payment_list=instance.paymentmethod.all()
	price_list_all=UserDetailsServicePrice.objects.filter(detail=instance)
	price_list_all_discount=UserDetailsServicePrice.objects.filter(detail=instance,servicepricediscount__gt=0)
	price_list_all_nodiscount=UserDetailsServicePrice.objects.filter(detail=instance).exclude(servicepricediscount__gt=0)
	discount_max=price_list_all.aggregate(Max('servicepricediscount'))
	timedict=instance.get_time_list_dict
	if discount_max["servicepricediscount__max"] is not None:
		discount_max_int =int(discount_max["servicepricediscount__max"])#dictionary 
	else:
		discount_max_int=0

	
	if rating_obj.exists():
		rating=rating_obj.first().rating

	else:
		rating=5    
	initial_data={
		"content_type":instance.get_content_type,
		"object_id":instance.id,
	}
	socialnetwork=UserDetailsSocialNetworks.objects.filter(detail=instance).first()
	sharestring=quote(instance.name+instance.surname)
	
	## trough model manager  
	comment_form=CommentForm(request.POST or None,initial=initial_data)
	if comment_form.is_valid():
		c_type=comment_form.cleaned_data.get("content_type")
		
		c_type=c_type.replace(" ", "")
		#ctype se dobije user details i nemoze nac nego morabit zajedno
		content_type=ContentType.objects.get(model=c_type)
		obj_id=comment_form.cleaned_data.get("object_id")
		parent_obj=None
		try:
			parent_id=int(request.POST.get("parent_id"))
		except:
			parent_id=None
		if parent_id:
			parent_qs=Comment.objects.filter(id=parent_id)
			if parent_qs.exists():
				parent_obj=parent_qs.first()


		content_data=comment_form.cleaned_data.get("content")
		new_comment,created =Comment.objects.get_or_create(
							user=request.user,
							content_type=content_type,
							object_id=obj_id,
							content=content_data,
							parent=parent_obj,
						)
		# print(new_comment.content_object.get_absolute_url_comments())
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url_comments())  
	#comments=Comment.objects.filter_by_instance(instance) #by query set and model manager in Comment model
	comments=instance.comments
	formdate=AppoitmentForm(None,None)
	if request.POST.get('appointment'): #iz name butona je add
		formdate=AppoitmentForm(request.POST or None)
		
		if formdate.is_valid():
			
			form_email=formdate.cleaned_data.get("email")
			form_message=formdate.cleaned_data.get("message")
			form_full_name=formdate.cleaned_data.get("name")
			form_full_surname=formdate.cleaned_data.get("surname")
			form_full_date=formdate.cleaned_data.get("date")
			form_full_phone=formdate.cleaned_data.get("phone")

			subject=_('Appoitment')
			from_email=settings.DEFAULT_FROM_EMAIL
			to_email= instance.email
			
			customer_email=form_email
			# contact_message="%s: %s via %s date: %s , phone: %s " %(form_full_name, form_message, form_email,form_full_date,form_full_phone )
			# subject, to = 'hello',  instance.email
			# text_content = 'This is an important message.'
			# html_content = '<p>This is an <strong>important</strong> message.</p>'+form_message
			# msg = EmailMultiAlternatives(subject, text_content, from_email, )
			# msg.attach_alternative(html_content, "text/html")
			template = get_template('email_template.html')
			
			context = {
			'subject': subject, 
			'customer_email': customer_email,
			'form_full_date':form_full_date,
			'form_full_phone':form_full_phone,
			'form_full_name':form_full_name,
			'form_full_surname':form_full_surname,
			'form_message' :form_message, 
			}
			content = template.render(context)
			
			msg = EmailMessage(subject, content, from_email, [to_email,'baal130@gmail.com'])
			msg.content_subtype = 'html'
			# FOR CUSTOMER 
			templatecustomer = get_template('email_template_to_customer.html')
			
			contextcustomer = {
			'subject': subject, 
			'doctor_email': instance.email,
			'form_full_date':form_full_date,
			'form_full_phone':instance.telefon,
			'form_full_name':instance.name,
			'form_full_surname':instance.surname,
			
			}
			contentcustomer = templatecustomer.render(contextcustomer)
			
			msgcustomer = EmailMessage(subject, contentcustomer, from_email, [customer_email])
			msgcustomer.content_subtype = 'html'

			try:
				
				msg.send()
				msgcustomer.send()
				messages.success(request,_('Your message has been send.We will send notice on your email'),extra_tags='')#message.tag salje sve tagove(npr sucess + extra tag) i loppa kao charachter stringa
				
			except:
				messages.error(request, _('Sorry,it is our fault. Message has not been send. Please send us a email or give us a call'),extra_tags='')
			
			
			
			return HttpResponseRedirect('/doctor/'+slug+'/')

		if formdate.errors:
			print(formdate.errors)	
	formcontact=ContactDoctorForm(None,None)
	if request.POST.get('contactdoctor'): #iz name butona je add
		formcontact=ContactDoctorForm(request.POST or None)
		
		if formcontact.is_valid():
			
			form_email=formcontact.cleaned_data.get("email")
			form_message=formcontact.cleaned_data.get("message")
			form_full_name=formcontact.cleaned_data.get("name")
			subject=formcontact.cleaned_data.get("subject")
			
			form_full_phone=formcontact.cleaned_data.get("phone")

			
			from_email=settings.EMAIL_HOST_USER
			to_email= instance.email
			
			customer_email=form_email
			template = get_template('email_template.html')
			
			context = {
			'subject': subject, 
			'customer_email': customer_email,
			
			'form_full_phone':form_full_phone,
			'form_full_name':form_full_name,
			
			'form_message' :form_message, 
			}
			content = template.render(context)
			
			msg = EmailMessage(subject, content, from_email, [to_email])
			msg.content_subtype = 'html'
			try:
				
				msg.send()
				messages.success(request,_('Your message has been send.We will send notice on your email'),extra_tags='')#message.tag salje sve tagove(npr sucess + extra tag) i loppa kao charachter stringa
				
			except:
				messages.error(request, _('Sorry,it is our fault. Message has not been send. Please send us a email or give us a call'),extra_tags='')
			
			
			
			return HttpResponseRedirect('/doctor/'+slug+'/')

		if formcontact.errors:
			print(formdate.errors)
					
	package_list=UserDetailsServicePackagePrice.objects.filter(detail=instance)
	language_list=UserDetailsLanguage.objects.filter(detail=instance)
	context={  
		"title":"doctor",
		"instance":instance,
		"comments":comments,
		"comment_form":comment_form,
		# "is_following":is_following,
		"slug":slug,
		"rating":rating,
		"rating_avg":rating_avg,
		"rating_avg_int":rating_avg_int,
		"galery_list":galery_list,
		"service_list_6":service_list_6,
		"service_list_all":service_list_all,
		"team_list":team_list,
		"department_list":department_list,
		"insurance_list":insurance_list,
		"payment_list":payment_list,
		"price_list_all":price_list_all,
		"price_list_all_discount":price_list_all_discount,
		"price_list_all_nodiscount":price_list_all_nodiscount,
		"discount_max_int":discount_max_int,
		"package_list":package_list,
		"language_list":language_list,
		"article_list":article_list,
		"socialnetwork":socialnetwork,
		"sharestring":sharestring,
		"timedict":timedict,
		"formdate":formdate,
		"formcontact":formcontact,
		
	}
	if extra_context is not None:
		context.update(extra_context)
	#return HttpResponse ("<h1> helo3  </h1>")
	# return render(request,"detaildoctor.html",context)
	return render(request,template,context)    

# u formi napraviti samo da se selektira service i doda se u objekt od package vraca se na taj package i mora bit edit packaga
@login_required
def user_detail_package(request):
	if not request.user.is_authenticated:
		raise Http404
	jsonDec = json.decoder.JSONDecoder()	
	user_detail_instance=UserDetails.objects.filter(user=request.user) #  instanca od detalja
	package_list=UserDetailsServicePackagePrice.objects.filter(detail__in=user_detail_instance)
	
	
	myPythonList =[]

	if user_detail_instance.exists():    # means alreday filled once this table  
		user_detail_instance=UserDetails.objects.get(user=request.user)
		# if user_detail_instance.verificated is  True:        #IF already verificated doesn't need to change anything more
		# 	#print(user_detail_instance.name)
		# 	title="ID verificated"
		# 	verificated=True
			
		# 	context={
		# 	"title":title,
			
		# 	"verificated":verificated,
		# 	}   
		# else:
		verificated=False
		title="Your ID is under verification"
		
		
		

	
		
		form=UserDetailsServicePackagePriceForm(None,None, user=user_detail_instance) #instance of the form
		
		if request.POST: 
			
				
			

			form= UserDetailsServicePackagePriceForm( request.POST or None, request.FILES or None, user=user_detail_instance  )
			if form.is_valid():
				
				newgallery=form.save(commit=False)
				newgallery.detail=user_detail_instance
				myPythonList.append(newgallery.selectservice.servicename)
				newgallery.service = json.dumps(myPythonList)
				# make list as array in text
				newgallery.save()
				package=UserDetailsServicePackagePrice.objects.get(pk=newgallery.pk)
				print(newgallery.pk)
				print(package.pk)	
				
				return redirect("newsletter:user_detail_package_update", pk=package.pk)
				  
		
		else:

			context={
			"form":form,
			"package_list":package_list,		
			"verificated":verificated,
			"title":title,
			
			} 
	else:
		title="Please fill in Your details for verification"
		form= UserWebDetailsForm( request.POST or None, request.FILES ) #instance of the form

		if form.is_valid(): 
			user_detail_instance=form.save(commit=False)
			user_detail_instance.user=request.user
			
			print(user_detail_instance.user)
			user_detail_instance.save()

		if form2.errors:
			print(form2.errors)

		 
		context={
		 "form":form,
		
		"title":title,
		} 

	return render(request,"user_detail_package.html",context)

def user_detail_package_update(request,pk):
	if not request.user.is_authenticated:
		raise Http404
	
				
	jsonDec = json.decoder.JSONDecoder()	
	user_detail_instance=UserDetails.objects.filter(user=request.user) #  instanca od detalja
	package=UserDetailsServicePackagePrice.objects.get(pk=pk)
	package_instance=UserDetailsServicePackagePrice.objects.filter(pk=pk)
	package_list=UserDetailsServicePackagePrice.objects.filter(detail__in=user_detail_instance)
	
	try:
		remark_list=UserDetailsServicePackagePriceRemark.objects.filter(userdetailsservicepackageprice__in=package_instance	)
	except:
		remark_list=None
	
		#tu treba uzet iz instance koja je za taj package
	packageTextList = jsonDec.decode(package.service)
	

	if user_detail_instance.exists():    # means alreday filled once this table  
		user_detail_instance=UserDetails.objects.get(user=request.user)
		# if user_detail_instance.verificated is  True:        #IF already verificated doesn't need to change anything more
		if False is  True: 
			#treba vidit kad je verificaran nis ne prikazuje)
			title="ID verificated"
			verificated=True
			print(verificated)
			context={
			"title":title,
			
			"verificated":verificated,
			}   
		else:
			verificated=False
			title="Your ID is under verification"
						
			form=UserDetailsServicePackagePriceForm(None,None,instance=package,user=user_detail_instance ) #instance of the form
			formremark= UserDetailsServicePackagePriceRemarkForm( request.POST or None, request.FILES or None)
			if request.POST.get('Add service'):
				form= UserDetailsServicePackagePriceForm( request.POST or None , request.FILES or None,instance=package,user=user_detail_instance)
				print(form)
				if form.is_valid():
					print("df")
					newgallery=form.save(commit=False)
					newgallery.detail=user_detail_instance
					packageTextList.append(newgallery.selectservice.servicename)
					newgallery.service = json.dumps(packageTextList)
					newgallery.save()
				if form.errors:
					print(form.errors)	

			if request.POST.get('Update package'):		 	
				print(request.POST)
				form= UserDetailsServicePackagePriceForm( request.POST or None, request.FILES or None,instance=package,user=user_detail_instance)
				if form.is_valid():
				
					newgallery=form.save(commit=False)
					newgallery.detail=user_detail_instance
					
					newgallery.save()
			if request.POST.get('Add package remark'):
						
				formremark= UserDetailsServicePackagePriceRemarkForm( request.POST or None, request.FILES or None)
				if formremark.is_valid():
				
						
					newremark=UserDetailsServicePackagePriceRemark()
					newremark=formremark.save(commit=False)
					newremark.userdetailsservicepackageprice=package
					newremark.save()	
			if request.is_ajax():
				formDataDescriptionText=request.POST.get('formDataDescriptionText') 
				
				
				
						
				newremark=UserDetailsServicePackagePriceRemark()
				newremark=formremark.save(commit=False)
				newremark.userdetailsservicepackageprice=package
				newremark.descriptionremark=formDataDescriptionText
				newremark.save()
				data = {
				"success": True,
				"newremark":formDataDescriptionText,
				}
				
				return JsonResponse(data)
				
			context={
			"form":form,
			"package_list":package_list,
			"formremark":formremark,
			"remarklist":remark_list,		
			"verificated":verificated,
			"title":title,
			"packageTextList":packageTextList,
			"package":package,
			} 
	else:
		title="Please fill in Your details for verification"
		form= UserWebDetailsForm( request.POST or None, request.FILES ) #instance of the form

		if form.is_valid(): 
			user_detail_instance=form.save(commit=False)
			user_detail_instance.user=request.user
			print("nesto")
			print(user_detail_instance.user)
			user_detail_instance.save()

		if form2.errors:
			print(form2.errors)

		 
		context={
		 "form":form,
		
		"title":title,
		} 

	return render(request,"user_detail_package.html",context)
	
def discount_detail(request, slug,template=None, extra_context=None): #retrieve
	
	instance=get_object_or_404(UserDetailsServicePackagePrice,slug=slug) 
	remark_instance=UserDetailsServicePackagePrice.objects.filter(slug=slug)
	
	try:
		remark_list=UserDetailsServicePackagePriceRemark.objects.filter(userdetailsservicepackageprice__in=remark_instance)
	except:
		remark_list=None
	jsonDec = json.decoder.JSONDecoder()	
	
	packageTextList = jsonDec.decode(instance.service)	
	
	formdate=AppoitmentForm(None,None)
	if request.POST.get('appointment'): #iz name butona je add
		formdate=AppoitmentForm(request.POST or None)
		
		if formdate.is_valid():
			
			form_email=formdate.cleaned_data.get("email")
			form_message=formdate.cleaned_data.get("message")
			form_full_name=formdate.cleaned_data.get("name")
			form_full_surname=formdate.cleaned_data.get("surname")
			form_full_date=formdate.cleaned_data.get("date")
			form_full_phone=formdate.cleaned_data.get("phone")

			subject='Appoitment'
			from_email=settings.EMAIL_HOST_USER
			to_email= instance.detail.email
			
			customer_email=form_email
			
			template = get_template('email_template_package.html')
			
			context = {
			'subject': subject, 
			'customer_email': customer_email,
			'form_full_date':form_full_date,
			'form_full_phone':form_full_phone,
			'form_full_name':form_full_name,
			'form_full_surname':form_full_surname,
			'form_message' :form_message, 
			'package_name':instance.name,
			'package_list':packageTextList,
			}
			content = template.render(context)
			
			msg = EmailMessage(subject, content, from_email, [to_email,'baal130@gmail.com'])
			msg.content_subtype = 'html'
			try:
				# send_mail(subject, 
				# contact_message, 
				# from_email,
				# [to_email], 
				# fail_silently=False )
				msg.send()
				messages.success(request,_('Your message has been send.We will send notice on your email'),extra_tags='')#message.tag salje sve tagove(npr sucess + extra tag) i loppa kao charachter stringa
				
			except:
				messages.error(request, _('Sorry,it is our fault. Message has not been send. Please send us a email or give us a call'),extra_tags='')
			
			
			
			return HttpResponseRedirect('/doctor/packages/'+slug+'/')

		if formdate.errors:
			print(formdate.errors)	
	context={  
		"formdate":formdate,
		"objects":instance,
		"remark_list":remark_list,
		"slug":slug,
		
		
	}
	if extra_context is not None:
		context.update(extra_context)
	
	return render(request,template,context) 
@login_required
def user_detail_social(request):
	if not request.user.is_authenticated:
		raise Http404
		
	user_detail_instance=UserDetails.objects.filter(user=request.user) #
	social_instance=UserDetailsSocialNetworks.objects.filter(detail__in=user_detail_instance).first()
	

	if user_detail_instance.exists():    
		user_detail_instance=UserDetails.objects.get(user=request.user)
		
		
						
		form=UserDetailsSocialNetworksForm( None, None,instance=social_instance) #instance of the form
		print(user_detail_instance)
		if request.POST: 
			form= UserDetailsSocialNetworksForm( request.POST or None, request.FILES or None,instance=user_detail_instance)
			if form.is_valid():
				
				newgallery=form.save(commit=False)
				newgallery.detail=user_detail_instance			
				newgallery.save()
			if form.errors:
				print(form.errors)		
		
				
			
		
			
	context={
	"form":form,}
	
			 
	

	return render(request,"user_detail_social.html",context)
