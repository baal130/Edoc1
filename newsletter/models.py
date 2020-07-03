from django.db import models

from django.conf import settings
from django.db.models.signals import post_save

from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.db.models import Q,Avg,Count
import googlemaps
from django.utils.translation import ugettext_lazy as _
import json
from django.core.validators import MaxValueValidator, MinValueValidator 
from comments.models import Comment 
from django.contrib.contenttypes.models import ContentType
from .languages import STATE_CHOICES
from bootstrap_datepicker_plus import DatePickerInput,TimePickerInput,DateTimePickerInput
from django.utils import timezone
from markdown_deux import markdown



User = settings.AUTH_USER_MODEL

Occupancy_CHOICES = (
	(_('Pacient'), _('PACIENT')),
	('Doctor','DOCTOR'),
	('STUDENT', 'STUDENT'),
	
)

Insurance_CHOICES = (
	('test1','test1'),
	('test2','test2'),
	
)
# Create your models here.
# models jednak databases u formama se oblikuju databasevi sto i kako se pretrazuje potrebno importirati odavde u formu
class Insurancecompany(models.Model):
	description = models.CharField(max_length=50,default='null',blank=True,)
	
	def __str__(self):
		return self.description 
	def __unicode__(self):
		return self.description
class Paymentmethod(models.Model):
	description = models.CharField(max_length=40,default='null',blank=True,)
	
	def __str__(self):
		return self.description 
	def __unicode__(self):
		return self.description


class SignUp(models.Model):
	email = models.EmailField()
	full_name = models.CharField(max_length=120,blank=False,null=False) #blank=false kada je potrebno unijeti polje
	timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
	updated = models.DateTimeField(auto_now_add=False,auto_now=True)

	def __unicode__(self):
		return self.email #ono sto se vidi u databasa kad gledamo ( u adminu npr)
 
class ProfileManager(models.Manager):
	def toggle_follow(self, request_user, username_to_toggle):
		profile_ = UserDetails.objects.get(user__username__iexact=username_to_toggle)
		user = request_user
		is_following = False
		if user in profile_.followers.all():
			profile_.followers.remove(user)
		else:
			profile_.followers.add(user)
			is_following = True
		return profile_, is_following
	# def active(self, *args, **kwargs):
	# 	return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())
def uplodad_location_gal(instance, filename):
	
	return "%s/%s" %(instance.detail.surname,filename)
def uplodad_location(instance, filename):
	
	return "%s/%s" %(instance.surname,filename)
def uplodad_location_package(instance, filename):
	
	return "%s/%s" %(instance.name,filename)
class UserDetails(models.Model):
	#user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	user               =models.OneToOneField(User, on_delete=models.CASCADE) #user.userdetails
	name 			   =models.CharField(max_length=60,blank=False,null=False)
	surname			   =models.CharField(max_length=60,blank=False,null=False)
	adress             =models.CharField(max_length=60,blank=False,null=False)
	city               =models.CharField(max_length=60,blank=False,null=False)
	state			   =models.CharField(max_length=40,choices=STATE_CHOICES,
										 blank=True)
	colony             =models.CharField(max_length=60,blank=True,null=True)
	telefon            =models.IntegerField(blank=True,null=True)
	startworkingtimeMonday=models.TimeField(auto_now_add=False,auto_now=False,default="08:00")
	endworkingtimeMonday=models.TimeField(auto_now_add=False,auto_now=False,default="17:00")
	mondaywork    =models.BooleanField(default=True)
	startworkingtimeTuesday=models.TimeField(auto_now_add=False,auto_now=False,default="08:00")
	tuesdaywork    =models.BooleanField(default=True)	
	endworkingtimeTuesday=models.TimeField(auto_now_add=False,auto_now=False,default="17:00")
	startworkingtimeWednesday=models.TimeField(auto_now_add=False,auto_now=False,default="08:00")
	wednesdaywork    =models.BooleanField(default=True)	
	endworkingtimeWednesday=models.TimeField(auto_now_add=False,auto_now=False,default="17:00")
	startworkingtimeThursday=models.TimeField(auto_now_add=False,auto_now=False,default="08:00")
	thursdaywork    =models.BooleanField(default=True)		
	endworkingtimeThursday=models.TimeField(auto_now_add=False,auto_now=False,default="17:00")
	startworkingtimeFriday=models.TimeField(auto_now_add=False,auto_now=False,default="08:00")	
	endworkingtimeFriday=models.TimeField(auto_now_add=False,auto_now=False,default="17:00")
	fridaywork    =models.BooleanField(default=True)	
	startworkingtimeSaturday=models.TimeField(auto_now_add=False,auto_now=False,default="08:00")
	endworkingtimeSaturday =models.TimeField(auto_now_add=False,auto_now=False,default="13:00")
	saturdaywork    =models.BooleanField(default=True)
	startworkingtimeSunday=models.TimeField(auto_now_add=False,auto_now=False,default="08:00")
	endworkingtimeSunday =models.TimeField(auto_now_add=False,auto_now=False,default="13:00")
	sundaywork    =models.BooleanField(default=False)
	insurancecompany   =models.ManyToManyField(Insurancecompany,blank=False,null=False)
	paymentmethod      =models.ManyToManyField(Paymentmethod)			 
						
	acceptpacients     =models.BooleanField(default=True)
	acceptanimales     =models.BooleanField(default=False)
	acceptchildren     =models.BooleanField(default=False)
	invalidsaccess     =models.BooleanField(default=False)
	englishspeaking	   =models.BooleanField(default=False)
	specialprice   	   =models.BooleanField(default=False)
	homevisit 		   =models.BooleanField(default=False)
	emergencycalls     =models.BooleanField(default=False) 	
	
	web				   =models.URLField(default='null')
	email              =models.EmailField(default='null',blank=True)
	verificated		   =models.BooleanField(default=False)
	IdentificationUser =models.FileField(null=False,blank=False)
	followers          =models.ManyToManyField(User, related_name='is_following', blank=True) # user.is_following.all()
	occupancy 		   =models.CharField(max_length=40,choices=Occupancy_CHOICES,
						default='Pacient',blank=True)
	speciality		   =models.CharField(max_length=60,
						blank=True)
	ratinghelp		   =models.IntegerField(default='5')
	ratingkind		   =models.IntegerField(default='5')
	ratingtime		   =models.IntegerField(default='5')
	ratingstaff		   =models.IntegerField(default='5')
	ratingethic		   =models.IntegerField(default='5')
	slug               =models.SlugField(unique=True)
	lat  		       =models.FloatField( blank=True, max_length=100,default=1.0)
	lng  		       =models.FloatField( blank=True, max_length=100,default=1.0)

	about    		   =models.TextField( blank=True)
	imagehome1 		   =models.ImageField(upload_to=uplodad_location,null=True,blank=True)
	imagehome2 		   =models.ImageField(upload_to=uplodad_location, null=True,blank=True)
	imagehome3 		   =models.ImageField(upload_to=uplodad_location, null=True,blank=True)
	imagehome1Text1    =models.CharField(max_length=60,blank=True,null=True)
	imagehome1Text2    =models.CharField(max_length=60,blank=True,null=True)
	imagehome2Text1    =models.CharField(max_length=60,blank=True,null=True)
	imagehome2Text2    =models.CharField(max_length=60,blank=True,null=True)
	imagehome3Text1    =models.CharField(max_length=60,blank=True,null=True)
	imagehome3Text2    =models.CharField(max_length=60,blank=True,null=True)
	profilepicture     =models.ImageField(upload_to=uplodad_location, null=True,blank=True)


	objects = ProfileManager()

	# def __unicode__(self):
	#  	return self.name #ono sto se vidi u databasa kad gledamo ( u adminu npr)
	def __str__(self):
		return self.user.username 
	def __unicode__(self):
		return self.user.username 

	def get_absolute_url(self):
		#return "/complain/%s/" %(self.id)
		#return reverse("dataadd:detail", kwargs={"id":self.id}) Za dynamicno prikazivanje urla
		return reverse("newsletter:doctor_detail", kwargs={"slug":self.slug}) # Za dynamicno prikazivanje urla
	def get_absolute_url_comments(self):
		
		return reverse("newsletter:comments", kwargs={"slug":self.slug}) # Za dynamicno prikazivanje urla	
	
		
			
	def get_total_rating(self):	
		instance=self
		rating_avg =instance.userdetailsrating_set.aggregate(Avg("rating"),Count("rating"))
		
		return rating_avg 
	def get_total_rating_help(self):	
		instance=self
		rating_avg =instance.userdetailsrating_set.aggregate(Avg("ratinghelp"),Count("ratinghelp"))
		return rating_avg
	def get_total_rating_kind(self):	
		instance=self
		rating_avg =instance.userdetailsrating_set.aggregate(Avg("ratingkind"),Count("ratingkind"))
		return rating_avg	
	def get_total_rating_time(self):	
		instance=self
		rating_avg =instance.userdetailsrating_set.aggregate(Avg("ratingtime"),Count("ratingtime"))
		return rating_avg
	def get_total_rating_staff(self):	
		instance=self
		rating_avg =instance.userdetailsrating_set.aggregate(Avg("ratingstaff"),Count("ratingstaff"))
		return rating_avg		
	def get_total_rating_ethic(self):	
		instance=self
		rating_avg =instance.userdetailsrating_set.aggregate(Avg("ratingethic"),Count("ratingethic"))
		return rating_avg
	def get_uses_discount(self):
		instance=self
		services=instance.userdetailsserviceprice_set.all()
		usesdicount=False
		for service in  services:
			if(service.servicepricediscount > 0):
				usesdicount=True
		return usesdicount
	@property 
	def comments(self):
		instance=self
		qs=Comment.objects.filter_by_instance(instance)
		return qs
	@property 
	def get_content_type(self):
		instance=self
		content_type=ContentType.objects.get_for_model(instance.__class__)
		return content_type
	def get_time_list_dict(self):
		# return dictionary as dict={1:{'days':['Mon','Fri'],'time':'17.30-19.00'},
     	# 						2:{'days':['thu','wed'],'time':'17.00-19.00'}}



		instance=self
		list_days=['mondaywork','tuesdaywork','wednesdaywork']
		dict={}
		dict[1]={}
		dicttemptime={}	
		dicttemptime[1]={}
		# for x in list_days:
		# newsletter.UserDetails.mondaywork (instance._meta.get_field(x))
		if instance.mondaywork:
			dict[1]['days']=['Monday']
			dict[1]['time']=str(instance.startworkingtimeMonday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeMonday.strftime("%H:%M"))
			
		if instance.tuesdaywork:
			dicttemptime[1]['time']=str(instance.startworkingtimeTuesday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeTuesday.strftime("%H:%M"))
			if dict[1]=={}:
				# first empty popuni dictionary
				dict[1]['days']=['Tuesday']
				dict[1]['time']=str(instance.startworkingtimeTuesday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeTuesday.strftime("%H:%M"))
			elif dicttemptime[1]['time']==dict[1]['time']:
				# same as monday
				dict[1]['days'].append('Tuesday')
			else:
				dict[2]={} #create nev dictionary with key
				dict[2]['days']=['Tuesday'] #create new pair
				dict[2]['time']=str(instance.startworkingtimeTuesday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeTuesday.strftime("%H:%M"))	
			
		if instance.wednesdaywork:
			dicttemptime[1]['time']=str(instance.startworkingtimeWednesday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeWednesday.strftime("%H:%M"))
			if dict[1]=={}:
				print("prvi prazan")
				dict[1]['days']=['Wednesday']
				dict[1]['time']=str(instance.startworkingtimeWednesday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeWednesday.strftime("%H:%M"))
			else:
				for k,v in dict.items():
					# trazi u dictionaryu isto vrijme i doda u listu
					foundsame=False
					if dicttemptime[1]['time']==dict[k]['time']:
						dict[k]['days'].append('Wednesday')
						print(k)
						foundsame=True
						break
				if 	not foundsame:	
					dict[k+1]={}
					dict[k+1]['days']=['Wednesday']
					dict[k+1]['time']=str(instance.startworkingtimeWednesday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeWednesday.strftime("%H:%M"))
			
					
		if instance.thursdaywork:
			dicttemptime[1]['time']=str(instance.startworkingtimeThursday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeThursday.strftime("%H:%M"))
			if dict[1]=={}:
				
				dict[1]['days']=['Thursday']
				dict[1]['time']=str(instance.startworkingtimeThursday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeThursday.strftime("%H:%M"))
			else:
				for k,v in dict.items():
					# trazi u dictionaryu isto vrijme i doda u listu
					foundsame=False
					if dicttemptime[1]['time']==dict[k]['time']:
						dict[k]['days'].append('Thursday')
						print(k)
						foundsame=True
						break
				if 	not foundsame:	
					dict[k+1]={}
					dict[k+1]['days']=['Thursday']
					dict[k+1]['time']=str(instance.startworkingtimeThursday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeThursday.strftime("%H:%M"))		 
		if instance.fridaywork:
			dicttemptime[1]['time']=str(instance.startworkingtimeFriday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeFriday.strftime("%H:%M"))
			if dict[1]=={}:
				
				dict[1]['days']=['Friday']
				dict[1]['time']=str(instance.startworkingtimeFriday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeFriday.strftime("%H:%M"))
			else:
				for k,v in dict.items():
					# trazi u dictionaryu isto vrijme i doda u listu
					foundsame=False
					if dicttemptime[1]['time']==dict[k]['time']:
						dict[k]['days'].append('Friday')
						print(k)
						foundsame=True
						break
				if 	not foundsame:	
					dict[k+1]={}
					dict[k+1]['days']=['Friday']
					dict[k+1]['time']=str(instance.startworkingtimeFriday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeFriday.strftime("%H:%M"))
		if instance.saturdaywork:
			dicttemptime[1]['time']=str(instance.startworkingtimeSaturday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeSaturday.strftime("%H:%M"))
			if dict[1]=={}:
				
				dict[1]['days']=['Saturday']
				dict[1]['time']=str(instance.startworkingtimeSaturday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeSaturday.strftime("%H:%M"))
			else:
				for k,v in dict.items():
					# trazi u dictionaryu isto vrijme i doda u listu
					foundsame=False
					if dicttemptime[1]['time']==dict[k]['time']:
						dict[k]['days'].append('Saturday')
						print(k)
						foundsame=True
						break
				if 	not foundsame:	
					dict[k+1]={}
					dict[k+1]['days']=['Saturday']
					dict[k+1]['time']=str(instance.startworkingtimeSaturday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeSaturday.strftime("%H:%M"))	
		if instance.sundaywork:
			dicttemptime[1]['time']=str(instance.startworkingtimeSunday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeSunday.strftime("%H:%M"))
			if dict[1]=={}:
				
				dict[1]['days']=['Saturday']
				dict[1]['time']=str(instance.startworkingtimeSunday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeSunday.strftime("%H:%M"))
			else:
				for k,v in dict.items():
					# trazi u dictionaryu isto vrijme i doda u listu
					foundsame=False
					if dicttemptime[1]['time']==dict[k]['time']:
						dict[k]['days'].append('Sunday')
						print(k)
						foundsame=True
						break
				if 	not foundsame:	
					dict[k+1]={}
					dict[k+1]['days']=['Sunday']
					dict[k+1]['time']=str(instance.startworkingtimeSunday.strftime("%H:%M"))+'-'+str(instance.endworkingtimeSunday.strftime("%H:%M"))								
		return dict	
		


class UserDetailsRating(models.Model):
	user               =models.ForeignKey(User,on_delete=models.CASCADE)
	detail             =models.ForeignKey(UserDetails,on_delete=models.CASCADE)
	rating             =models.FloatField(default='5.0')
	ratinghelp		   =models.IntegerField(default='5')
	ratingkind		   =models.IntegerField(default='5')
	ratingtime		   =models.IntegerField(default='5')
	ratingstaff		   =models.IntegerField(default='5')
	ratingethic		   =models.IntegerField(default='5')

	def __unicode__(self):
		return "%s" %(self.rating)
	def __str__(self):
		return "%s" %(self.rating) + self.user.username

class UserDetailsFeatured(models.Model):
	
	detail             =models.ForeignKey(UserDetails,on_delete=models.CASCADE)
	rating             =models.FloatField(default=0)
	

	def __unicode__(self):
		return "%s" %(self.rating)
	def __str__(self):
		return "%s" %(self.rating) + self.detail.surname	

class UserDetailsGallery(models.Model):
	detail             =models.ForeignKey(UserDetails,on_delete=models.CASCADE)
	imagehomegallery   =models.ImageField(upload_to=uplodad_location_gal, null=True,blank=True)

	def __unicode__(self):
		return self.detail.surname
	def __str__(self):
		return self.detail.surname
class UserDetailsService(models.Model):
	detail             =models.ForeignKey(UserDetails,on_delete=models.CASCADE)
	flavicon           =models.CharField(max_length=60,blank=True,null=True)
	servicename        =models.CharField(max_length=60,blank=False,null=False)
	servicetext        =models.TextField(max_length=120,blank=True)
	weburl             =models.URLField(blank=True)


	def __unicode__(self):
		return self.detail.surname
	def __str__(self):
		return self.servicename
class UserDetailsServiceSearch(models.Model):
	#used for generating sevices which can be searched
	servicename        =models.CharField(max_length=60,blank=False,null=False)
	


	
	def __str__(self):
		return self.servicename
class UserDetailsDepartment(models.Model):
	detail             =models.ForeignKey(UserDetails,on_delete=models.CASCADE)
	imagehomedep 		   =models.ImageField(upload_to=uplodad_location_gal, null=True,blank=True)
	weburl             =models.URLField(blank=True)
	departmentname     =models.CharField(max_length=60,blank=True,null=True)
	departmenttext     =models.TextField(max_length=120,blank=True)
	def __unicode__(self):
		return self.detail.surname
	def __str__(self):
		return self.detail.surname
class UserDetailsTeam(models.Model):
	detail             =models.ForeignKey(UserDetails,on_delete=models.CASCADE)
	imagehometeam 	   =models.ImageField(upload_to=uplodad_location_gal, null=True,blank=True)
	weburl             =models.URLField(blank=True)
	teamname     	   =models.CharField(max_length=60,blank=True,null=True)
	teamtext           =models.TextField(max_length=120,blank=True)
	def __unicode__(self):
		return self.detail.surname
	def __str__(self):
		return self.detail.surname
class UserDetailsServicePrice(models.Model):
	detail            	 	=models.ForeignKey(UserDetails,on_delete=models.CASCADE)
	service 		   		=models.ForeignKey(UserDetailsService,on_delete=models.CASCADE)
	serviceprice       		=models.IntegerField(max_length=10,blank=True,null=True)
	servicepricediscount    =models.IntegerField(max_length=3,blank=True,null=True,validators=[MinValueValidator(0), MaxValueValidator(100)],default=0)
	def __str__(self):
		return  self.service.servicename
	def detail_name(self):
		return self.detail.surname	
	 #za admin drugacije zove
	def discounted_price(self):
		if self.servicepricediscount > 0 :
			x=self.serviceprice*self.servicepricediscount/100
			price=self.serviceprice-x
		else:
			price=self.serviceprice
		
		return price
class UserDetailsLanguage(models.Model):
		detail            	 	=models.ForeignKey(UserDetails,on_delete=models.CASCADE)
		language        		=models.CharField(max_length=20,blank=True,null=True)

class UserDetailsServicePackagePrice(models.Model):
	detail            	 	=models.ForeignKey(UserDetails,on_delete=models.CASCADE)
	selectservice 		   	=models.ForeignKey(UserDetailsService,on_delete=models.CASCADE)
	service 		   		=models.TextField(null=True,blank=True)
	totalregularprice		=models.IntegerField(max_length=10,blank=True,null=True)
	packagepricediscount    =models.IntegerField(max_length=10,blank=True,null=True,validators=[MinValueValidator(0), MaxValueValidator(100)])
	name                    =models.CharField(max_length=60,blank=True,null=True)
	headdescription         =models.TextField(null=True,blank=True)
	description             =models.TextField(null=True,blank=True)
	packageimage 		    =models.ImageField(upload_to=uplodad_location_package, null=True,blank=True)
	extragift				=models.TextField(null=True,blank=True)
	offerends               =models.DateTimeField(null=True,blank=True)
	offerstarts             =models.DateTimeField(null=True,blank=True)
	slug               		=models.SlugField(unique=False)
	def __str__(self):
		return  self.selectservice.servicename
	def get_service_list(self):
		instance=self
		jsonDec = json.decoder.JSONDecoder()
		# ["name1", "name2"] service je text field lista
		packageTextList = jsonDec.decode(instance.service)	
		return packageTextList
	def get_discount_price(self):
		instance=self
		try:
			discounted_price=round(instance.totalregularprice-(instance.totalregularprice*instance.packagepricediscount/100))
		except:
		
			discounted_price=instance.totalregularprice
		
		
		return 	discounted_price
	def get_time_left(self):
		instance=self
		deltatime=instance.offerends-timezone.now()
		days=deltatime.days
		hours=deltatime.seconds//3600#// // is used instead of / to get an integer, not a float. // is a floor division operator
		minutes=(deltatime.seconds//60)%60
		return "%s days: %s hours: %s minutes " %(days,hours,minutes) 
	def get_markdown(self):
		content=self.description
		return mark_safe(content) # for sumernote content already html
		# return mark_safe(markdown(content)) # for pagedown is ok
		
	def get_absolute_url(self):
		
		return reverse("newsletter:discount_detail", kwargs={"slug":self.slug}) 

class UserDetailsServicePackagePriceRemark(models.Model):
	
	userdetailsservicepackageprice =models.ForeignKey(UserDetailsServicePackagePrice,on_delete=models.CASCADE)
	descriptionremark             =models.CharField(null=True,blank=True, max_length=100)
	
	def __str__(self):
		
		return "%s/%s" %(self.userdetailsservicepackageprice.name,self.userdetailsservicepackageprice.detail.name)
class UserDetailsSocialNetworks(models.Model):
	detail            	 	=models.ForeignKey(UserDetails,on_delete=models.CASCADE)
	facebookurl             =models.URLField(blank=True)
	linkedinurl             =models.URLField(blank=True)
	twitterurl              =models.URLField(blank=True)
	instagramurl			=models.URLField(blank=True)
	pinteresturl			=models.URLField(blank=True)
	youtubeurl				=models.URLField(blank=True)
	behanceurl				=models.URLField(blank=True)
	whatsupnumber			=models.IntegerField(blank=True,null=True,default='0')

	def __unicode__(self):
		return self.detail.surname
	def __str__(self):
		return self.detail.surname
def post_save_user_receiver(sender, instance, created, *args, **kwargs):
	if created:
		profile, is_created = UserDetails.objects.get_or_create(user=instance)
		# default_user_profile =UserDetails.objects.get_or_create(user__id=1)[0] #user__username=
		# default_user_profile.followers.add(instance)
		#profile.followers.add(default_user_profile.user)
		#profile.followers.add(2)

post_save.connect(post_save_user_receiver, sender=User)

def create_slug(instance, new_slug=None):
	slug=slugify(instance.user)
	if new_slug is not None:
		slug=new_slug
	qs=UserDetails.objects.filter(slug=slug).order_by("-id")
	exists=qs.exists()
	if exists:
		new_slug= "%s-%s" %(slug,qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug
def pre_save_details_receiver(sender,instance, *args, **kwargs):
	# when userdetails is created( with pre save of users(IDiots model) or changed update or create new slug)
	
	
	if not instance.slug:
		instance.slug =create_slug(instance)
	else:
		instance.slug =update_slug(instance)

	

	# print(instance.slug)
	# need to use later
	try:
		gmaps = googlemaps.Client(key='AIzaSyAqOazqPcP8E-_s-Vp7MRbP3UMUgS2xfQw')	
		geocode_result = gmaps.geocode(instance.adress+instance.city+instance.colony)
		# print(geocode_result)
		# print(geocode_result[0]['geometry']['location']['lat'])
		instance.lat=geocode_result[0]['geometry']['location']['lat']
		instance.lng=geocode_result[0]['geometry']['location']['lng']
	except:
		pass	
pre_save.connect(pre_save_details_receiver, sender=UserDetails)


def pre_save_service_receiver(sender,instance, *args, **kwargs):
	
	# SERVICE_LIST = getattr(settings, 'SERVICE_LIST','')
	servicelist=UserDetailsServiceSearch.objects.all()
	add=True
	for service in servicelist:
		if instance.servicename==service.servicename:
			add=false
	if add:		
		i=UserDetailsServiceSearch()
		i.servicename=instance.servicename
		i.save()
	# SERVICE_LIST.append(instance.servicename)
	 


pre_save.connect(pre_save_service_receiver, sender=UserDetailsService)



def update_slug(instance, new_slug=None):
	slug=slugify(instance.name + instance.surname)

	return slug

def create_slug_package(instance, new_slug=None):
	slug=slugify(instance.name)
	if new_slug is not None:
		slug=new_slug
	qs=UserDetailsServicePackagePrice.objects.filter(slug=slug).order_by("-id")
	exists=qs.exists()
	if exists:
		new_slug= "%s-%s" %(slug,qs.first().id)
		return create_slug_package(instance, new_slug=new_slug)
	return slug
def update_slug_package(instance, new_slug=None):
	slug=slugify(instance.name)
	
	return slug	
def pre_save_discount_receiver(sender,instance, *args, **kwargs):
	
	
	if not instance.slug:
		instance.slug =create_slug_package(instance)
	else:
		instance.slug =update_slug_package(instance)

pre_save.connect(pre_save_discount_receiver, sender=UserDetailsServicePackagePrice)