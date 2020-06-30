from django import forms
from pagedown.widgets import PagedownWidget
from markdownx.fields import MarkdownxFormField
from .models import Idiot
from datetimewidget.widgets import DateTimeWidget
from datetime import date
from django.utils import timezone
from ckeditor.fields import RichTextField
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from django.utils.translation import ugettext_lazy as _

class IdiotForm(forms.ModelForm):  #koristi se form iz modela 
	description=forms.CharField(widget=PagedownWidget())
	description=forms.CharField(widget=SummernoteInplaceWidget())
	# description= MarkdownxFormField()
	# description=RichTextField()
	publish=forms.DateField(
		widget=forms.SelectDateWidget,initial=timezone.now())
	class Meta:     # na koji model se form odnosi 
		model = Idiot
		
		fields = [ 'company_name' , 'description', 'draft','publish',] # iz signup modela(database) varijabel
		labels = {
			'company_name': _('Article title'),
			'draft': _('Draft - Save Your post for later'),
			'publish': _('Publish - Select date when Post will be published'),
			# 'name_visible': _('Select if you want to show your name with post'),
			# 'image': _('Upload files to prove Your statements'),
			# 'article':_('Use text as article for general info'),
			
		}
		initials = {
			'company_name': _('Title what is about article.'),
			'description': _('Create here new article'),
		}

	  

		###
class NewsForm(forms.ModelForm):  #koristi se form iz modela 
	description=forms.CharField(widget=PagedownWidget())
	description=forms.CharField(widget=SummernoteInplaceWidget())
	# description= MarkdownxFormField()
	# description=RichTextField()
	publish=forms.DateField(
		widget=forms.SelectDateWidget,initial=timezone.now())
	class Meta:     # na koji model se form odnosi 
		model = Idiot
		
		fields = [ 'company_name' , 'description','image', 'draft','name_visible','publish','cities','news'] # iz signup modela(database) varijabel
		labels = {
			'company_name': _('Punch  or news name'),
			'draft': _('Draft - Save Your post for later'),
			'publish': _('Publish - Select date when Post will be published'),
			'name_visible': _('Publish - Select date when Post will be published'),
			'image': _('Upload files to prove Your statements'),
			'news':_('Use text as news fos site'),
			
		}
		initials = {
			'company_name': _('Some useful help text.'),
		}

	  

		###

class IdiotFormDetails(forms.ModelForm):  #koristi se form iz modela 
	class Meta:     # na koji model se form odnosi 
		model = Idiot
		fields = [ 'name' , 'surname','city', 'adress',] # iz signup modela(database) varijabel
		###


class CategoryForm(forms.ModelForm):  #
	class Meta:     # na koji model se form odnosi 
		model = Idiot
		
		fields = [ 'cities'] 
		labels = {
			'cities': _('CITIES'),
			

		}  