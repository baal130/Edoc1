from django import forms
from django.conf import settings

from .models import SignUp,UserDetails,UserDetailsGallery,UserDetailsService,UserDetailsDepartment,UserDetailsTeam,Insurancecompany
from .models import  Paymentmethod,UserDetailsServicePrice,UserDetailsServicePackagePrice,UserDetailsLanguage,UserDetailsServiceSearch
from .models import UserDetailsSocialNetworks,UserDetailsServicePackagePriceRemark
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import Select2MultipleWidget
from django.forms.widgets import  NumberInput,HiddenInput,TextInput,Select,TimeInput
from datetimewidget.widgets import DateTimeWidget
from datetime import date
from .languages import Language_CHOICES,Favicon_CHOICES,STATE_CHOICES,CITY_CHOICES,Specialty_CHOICES
from bootstrap_datepicker_plus import DatePickerInput,TimePickerInput,DateTimePickerInput
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from pagedown.widgets import PagedownWidget
from django.core.validators import RegexValidator

class ContactForm(forms.Form): # koristi se fform odavde
	full_name=forms.CharField( required=False)
	email=forms.EmailField()
	message= forms.CharField(widget=forms.Textarea)
		
class AppoitmentForm(forms.Form): # koristi se fform odavde
	name=forms.CharField( required=False)
	surname=forms.CharField( required=False)
	email=forms.EmailField(required=False)
	
	date=forms.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS,widget=DateTimePickerInput())
	phone=forms.CharField( required=False)
	message= forms.CharField(required=False,widget=forms.Textarea)

class ContactDoctorForm(forms.Form): # koristi se fform odavde
	name=forms.CharField( required=False)
	email=forms.EmailField(required=False)
	phone=forms.CharField( required=False)
	subject=forms.CharField( required=False)
	
	
	message= forms.CharField(required=False,widget=forms.Textarea)	
class ContactDoctorInListForm(forms.Form): # koristi se fform odavde
	name=forms.CharField( required=False)
	email=forms.EmailField(required=False)
	phone=forms.CharField( required=False)
	subject=forms.CharField( required=False)
	message= forms.CharField(required=False,widget=forms.Textarea)	
	




class SignUpForm(forms.ModelForm):  #koristi se form iz modela 
	class Meta:     # na koji model se form odnosi 
		model = SignUp
		fields = [ 'full_name' , 'email'] # iz signup modela(database) varijabel
		###
	
	# def clean_email(self): #za validaciju
	# 	#print =self.cleaned.data
	# 	email= self.cleaned_data.get('email')
	# 	email_base,provider = email.split("@")
	# 	domain,extension = provider.split('.')
	# 	if not extension == "edu":
	# 	#if not "edu" in email:
	# 		raise forms.ValidationError("Please use edu")
	# 	return email

	#def clean_full_name(self):
	#	full_name = self.cleaned_data.get('full_name')
	#	if not "kita" in full_name:
	#		raise forms.ValidationError("please use kita")
				
	#	return full_name
class UserDetailsForm(forms.ModelForm):  #koristi se form iz modela 
	speciality=forms.ChoiceField(
					choices=Specialty_CHOICES)  
	
	telefon = forms.CharField(min_length=7, validators=[RegexValidator(r'^\+\d{8,15}$', message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))])
	class Meta:     
		model = UserDetails
		fields = [ 'name' , 'surname','adress','city','colony','state', 'telefon','web','email',
				  'speciality', 'IdentificationUser','profilepicture',] 
		labels = {'name': _('Your first name'),
				  'surname': _('Your second name'),
				  'adress': _('Address'),
				  'city': _('City'),
				  
				  'state': _('State'),
				  
				  'speciality': _('Speciality'),
				  'IdentificationUser': _('Document for identification doctor'),
				  'profilepicture': _('Profile picture 480x480'),
				

		}		  
		widgets = {
		   
		}
	
class UserWebDetailsForm(forms.ModelForm):  #koristi se form iz modela 
	# imagehome1Text1 = forms.CharField( widget=forms.TextInput(label=_('First Title'),attrs={'placeholder': 'Enter Title'}))
	
	class Meta:     
		model = UserDetails
		fields = [ 'about' , 'imagehome1','imagehome1Text1','imagehome1Text2','imagehome2','imagehome2Text1','imagehome2Text2',
					'imagehome3','imagehome3Text1','imagehome3Text2'
				 ] 
		
		labels = {'about': _('Write about yourself'),
			'imagehome1': _('Choose Picture for first top image, size: 1920x880px'),
			'imagehome1Text1': _('First Title'),
			'imagehome1Text2': _('Second Title'),
			'imagehome2': _('Choose Picture for second top image, size: 1920x880px'),
			'imagehome2Text1': _('First Title'),
			'imagehome2Text2': _('Second Title'),
			'imagehome3': _('Choose Picture for third top image, size: 1920x880px'),
			'imagehome3Text1': _('First Title'),
			'imagehome3Text2': _('Second Title'),	

		}
		widgets = {
			'about': forms.Textarea(attrs={'placeholder': _('Enter text about you'),'class':'test'}),
			'imagehome1Text1': forms.TextInput(attrs={'placeholder': 'Enter first title with first image'}),
			'imagehome1Text2': forms.TextInput(attrs={'placeholder': 'Enter second title with first image'}),
			'imagehome2Text1': forms.TextInput(attrs={'placeholder': 'Enter first title with second image'}),
			'imagehome2Text2': forms.TextInput(attrs={'placeholder': 'Enter second title with second image'}),
			'imagehome3Text1': forms.TextInput(attrs={'placeholder': 'Enter first title with third image'}),
			'imagehome3Text2': forms.TextInput(attrs={'placeholder': 'Enter second title with third image'}),
		}
		###	
class UserDetailsGalleryForm(forms.ModelForm):  #koristi se form iz modela 
	
	# imagehome3=forms.ImageField(widget=forms.FileInput(attrs={'class': 'te','id': 'files'}))
	class Meta:     
		model = UserDetailsGallery
		fields = ['imagehomegallery'] 

		labels = {
			'imagehomegallery': _('Choose Picture for Gallery size 480x480'),
				
		}

class UserDetailsServiceForm(forms.ModelForm):  #koristi se form iz modela 
	# imagehome1Text1 = forms.CharField( widget=forms.TextInput(label=_('First Title'),attrs={'placeholder': 'Enter Title'}))
	flavicon=forms.ChoiceField(widget=forms.RadioSelect,choices=Favicon_CHOICES)

	# flavicon = forms.MultipleChoiceField( mora ic s manytomany field
 #        required=False,
 #        widget=forms.CheckboxSelectMultiple,
 #        choices=Favicon_CHOICES,
 #    )
	class Meta:    
		model = UserDetailsService
		fields = [ 'flavicon' , 'servicename','servicetext','weburl'
				 ] 
		
		labels = {'servicetext': _('Service description'),
				   'servicename': _('Service'),
		}
		widgets = {
			'servicename': forms.TextInput(attrs={'placeholder': _('Enter Service name')}),
			'servicetext': forms.Textarea(attrs={'placeholder': _('Enter text about service')}),
			'weburl': forms.URLInput(attrs={'placeholder': _('Enter your web page url to this service')}),
		}
class UserDetailsDepartmentForm(forms.ModelForm): 
	
	class Meta:   
		model = UserDetailsDepartment
		fields = [ 'departmentname' , 'departmenttext','imagehomedep','weburl'
				 ] 
		
		labels = {'departmenttext': _('Department description'),
				   'departmentname': _('Department name'),
				   'imagehomedep': _('Choose Picture for Department size 605x442'),
		}
		widgets = {
			'departmentname': forms.TextInput(attrs={'placeholder': _('Enter department name')}),
			'departmenttext': forms.Textarea(attrs={'placeholder': _('Enter text about department ex:The Dental Clinic program tremendously affects patients lives," said Dr. Mathew. or Cardiology is the branch of medicine that studies and deals with heart problems.')}),
			
			'weburl': forms.URLInput(attrs={'placeholder': _('Enter your web page url to this department')}),
		}
class UserDetailsTeamForm(forms.ModelForm): 
		   

	class Meta:   
		model = UserDetailsTeam
		fields = [ 'imagehometeam' , 'teamname','teamtext'
				 ] 
		
		
		labels = {'teamtext': _('Doctor description'),
				   'teamname': _('Doctor name'),
				   'imagehometeam': _('Choose Picture for Team member  size 450x450'),
		}
		widgets = {
			'teamname': forms.TextInput(attrs={'placeholder': _('Enter Doctor member name')}),
			'teamtext': forms.Textarea(attrs={'placeholder': _('Enter text about doctor in team')}),
			
		}
class UserDetailsInsuranceForm(forms.ModelForm): 
	# insurancecompany= forms.ModelMultipleChoiceField(
	# 		        required=False,
	# 		        widget=forms.CheckboxSelectMultiple,
	# 		        queryset=Insurancecompany.objects.all()
	insurancecompany= forms.ModelMultipleChoiceField(
					required=False,
					widget=Select2MultipleWidget,
					queryset=Insurancecompany.objects.all(),
					label = _('Choose Insurance company accepted (hold ctrl to select more options)'),		    )       
	#mora postojat instanca modela insuracne company da bi se moglo selektirat 
	class Meta:   
		model = UserDetails
		fields = [ 'insurancecompany', 
			 ] 
		labels = {'insurancecompany': _('Select Insurancecompany (hold ctrl to select more options)'),
				   
		}	 
class UserDetailsLanguageForm(forms.ModelForm): 
		  
	language=forms.ChoiceField(choices= Language_CHOICES)	   
	class Meta:   
		model = UserDetailsLanguage
		fields = [ 'language' , 
				 ] 
		
		
		labels = {'language': _('Spoken language'),
				   
		}
		widgets = {
			
			
		}				 
class PaymentmethodForm(forms.ModelForm): 
	# insurancecompany= forms.ModelMultipleChoiceField(
	# 		        required=False,
	# 		        widget=forms.CheckboxSelectMultiple,
	# 		        queryset=Insurancecompany.objects.all()
	paymentmethod= forms.ModelMultipleChoiceField(
					required=False,
					widget=Select2MultipleWidget,
					queryset=Paymentmethod.objects.all(),
					label = _('Choose Payment method (hold ctrl to select more options)'),		    )       
	#mora postojat instanca modela insuracne company da bi se moglo selektirat 
	class Meta:   
		model = UserDetails
		fields = [ 'paymentmethod', 
				 ] 		
		
class UserDetailsExtraForm(forms.ModelForm):  
	
	class Meta:     
		model = UserDetails
		fields = [ 'acceptchildren','invalidsaccess', 'specialprice', 'acceptanimales', 'homevisit','patientnumber','awardnumber',
				 ] 
	
		labels = {'acceptchildren': _('Also examines children up to 12 years '),
			'invalidsaccess': _('Access for people with disabilities'),
			'specialprice': _('Do you want to use discount prices with Todos doctors'),
			'acceptanimales': _('Pacients can come with animales'),
			'homevisit': _('Do you make home visits to patients'),
			'patientnumber': _('Enter how much patients approximately you have'),	
			'awardnumber': _('If you have any awards enter how much '),		

		}
		widgets = {
		   
		}


class UserDetailsServicePriceForm(forms.ModelForm):
	
		
	class Meta:     
		model = UserDetailsServicePrice

		fields= ['service','serviceprice','servicepricediscount',]

		labels = {'serviceprice': _('Regular price of service'),'servicepricediscount': _('Discount  on service'),
		}
		widgets = {
					'service': Select(attrs={'disabled':'disabled'}),
					'serviceprice': NumberInput(attrs={'placeholder': _('Enter regular price')}),
					'servicepricediscount': NumberInput(attrs={'placeholder': _('Enter discount for regular price in %')}),

					}
	def __init__(self, *args, **kwargs):
		super(UserDetailsServicePriceForm, self).__init__(*args, **kwargs)
		self.fields['service'].required = False
			# if instance and instance.id   if ako npr postoji  a ne zelimo mijenjat vise
						# da bi uspili snimit foreign key koje je po defaultu required moram stavit da nije required
						# poslije toga moramo stavit nazad u bazu vrijednost koja je bila 
	def clean_service(self):
		instance = getattr(self, 'instance', None)
		print(instance.service)
		# if instance:
		return instance.service
		# else:
		# 	return self.cleaned_data.get('service', None)	
class UserDetailsServicePackagePriceForm(forms.ModelForm):  
	


	description=forms.CharField(widget=PagedownWidget())
	description=forms.CharField(widget=SummernoteInplaceWidget())
	class Meta:     
		model = UserDetailsServicePackagePrice
		fields = [ 'name','packagepricediscount','totalregularprice','headdescription','description','packageimage',
					'extragift','offerstarts', 'offerends','selectservice',
				 ] 
	
		labels = {'selectservice': _('Add service to package '),
				  'packagepricediscount': _(' Discount on this total price % '),
				  'totalregularprice': _(' Total regular price for services in package '),
				  'name': _(' Package name '),
				  'headdescription':_('Head title description'),
				  'description':_('Detailed description of your package'),
				  'packageimage':_('Use image with your package'),
				  'extragift':_('Add gift for promotion'),
				  'offerends':_('Until when offer is valid'),
				  'offerstarts':_('From when offer is valid'),
		}
		widgets = {
		   'packagepricediscount': NumberInput(attrs={'placeholder': _('Enter discount percentage for services  price in %')}),
			'totalregularprice': NumberInput(attrs={'placeholder': _('Enter total price for services  price in $')}),
			'name': forms.TextInput(attrs={'placeholder': _('Enter name of package')}),
			'headdescription': forms.Textarea(attrs={'placeholder': _('Add most important overview of your package.It will be visible with list of packages and on begginning')}),
			'description': forms.Textarea(attrs={'placeholder': _('Write some interesting details about your offer')}),
			'offerends':DatePickerInput(),	
			'offerstarts':DatePickerInput(),	
			'extragift': forms.TextInput(attrs={'placeholder': _('Add extra gift outside sevice ex: Free smile or free apartment for 2 days')}),	
			 
		}
		initials = {
			
			
		}
	def __init__(self ,*args, **kwargs):
		user= kwargs.pop('user') #ovo mora bit ako se salje novi argument
		super(UserDetailsServicePackagePriceForm, self).__init__(*args, **kwargs)
		# access object through self.instance...
		print(user)
		
		self.fields['selectservice'].queryset = UserDetailsService.objects.filter(detail=user)
class UserDetailsServicePackagePriceRemarkForm(forms.ModelForm): 
	class Meta:     
		model = UserDetailsServicePackagePriceRemark
		fields = [ 'descriptionremark',
					
				 ] 
	
		labels = {
				  'descriptionremark':_('Add remarks for your package'),
				  
		}
		widgets = {
		   
			 
		}
		initials = {
			
			'descriptionremark': _('Add remark which is important for use your package '),
		}				
class UserDetailsSearchStateForm(forms.ModelForm):  
	class Meta:     # na koji model se form odnosi 
		model = UserDetails
		
		fields = [ 'state'] 
		labels = {
			'state': _(''),
			

		} 	
class UserDetailsSearchCitiesForm(forms.Form):  
	city=forms.ChoiceField(
					choices=CITY_CHOICES,label='')
	
	def __init__(self, *args, **kwargs):
		super(UserDetailsSearchCitiesForm, self).__init__(*args, **kwargs)
		self.fields['city'].required = False		

		 
class UserDetailsSearchSpecialityForm(forms.Form):  
	speciality=forms.ChoiceField(
					choices=Specialty_CHOICES,label='')
	def __init__(self, *args, **kwargs):
		super(UserDetailsSearchSpecialityForm, self).__init__(*args, **kwargs)
		self.fields['speciality'].required = False
class UserDetailsSearchServiceForm(forms.Form):  
	object_list=UserDetailsServiceSearch.objects.all()
	Service_CHOICES=[('', _('Select_service')),]
	try :
		for service in object_list:
			Service_CHOICES.append((service.servicename,service.servicename))
	except:
		pass
	service=forms.ChoiceField(
					choices=Service_CHOICES,label='')			
	def __init__(self, *args, **kwargs):
		super(UserDetailsSearchServiceForm, self).__init__(*args, **kwargs)
		self.fields['service'].required = False

class UserDetailsFormTime(forms.ModelForm):  #koristi se form iz modela 
	
	

	class Meta:     
		model = UserDetails
		fields = [  'startworkingtimeMonday','endworkingtimeMonday','mondaywork',
			'startworkingtimeTuesday','endworkingtimeTuesday','tuesdaywork',
			'startworkingtimeWednesday','endworkingtimeWednesday','wednesdaywork',
			'startworkingtimeThursday','endworkingtimeThursday','thursdaywork',
			'startworkingtimeFriday','endworkingtimeFriday','fridaywork',
			'startworkingtimeSaturday','endworkingtimeSaturday','saturdaywork',
			'startworkingtimeSunday','endworkingtimeSunday','sundaywork',
				  ] 
		widgets = {
			
			'startworkingtimeMonday': TimePickerInput(attrs={"class": "test"}),
			'endworkingtimeMonday': TimePickerInput(),
			'startworkingtimeTuesday': TimePickerInput(attrs={ }),
			'endworkingtimeTuesday': TimePickerInput(attrs={}),
			'startworkingtimeWednesday': TimePickerInput(attrs={ }),
			'endworkingtimeWednesday': TimePickerInput(attrs={}),
			'startworkingtimeThursday': TimePickerInput(attrs={ }),
			'endworkingtimeThursday': TimePickerInput(attrs={}),

			'startworkingtimeFriday': TimePickerInput(attrs={ }),
			'endworkingtimeFriday': TimePickerInput(attrs={}),
			'startworkingtimeSaturday': TimePickerInput(attrs={ }),
			'endworkingtimeSaturday': TimePickerInput(attrs={}),
			'startworkingtimeSunday': TimePickerInput(attrs={ }),
			'endworkingtimeSunday': TimePickerInput(attrs={}),
		}		

class UserDetailsSocialNetworksForm(forms.ModelForm):  
	
	class Meta:     
		model = UserDetailsSocialNetworks
		fields = [ 'facebookurl','linkedinurl','twitterurl','instagramurl','pinteresturl','youtubeurl','behanceurl',
					'whatsupnumber'
				 ] 
	
		labels = {'facebookurl': _('Add link to your facebook page '),
				  'linkedinurl': _('Add link to your linkedin page '),  
				  'twitterurl': _('Add link to your twitter page '),
				  'instagramurl': _('Add link to your instagram page '),
				  'pinteresturl': _('Add link to your pinterest page '),
				  'youtubeurl': _('Add link to your youtube page '),  
				  'behanceurl': _('Add link to your behance page '),
				  'whatsupnumber': _('Add your whatsupnumber '),
				  }	
					
	