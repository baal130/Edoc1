from django.contrib import admin
from allauth.account.models import EmailAddress
# Register your models here for admin 
#from .forms import SignUpForm 
from .models import SignUp,UserDetails,UserDetailsRating,UserDetailsGallery,UserDetailsService
from .models import UserDetailsDepartment,UserDetailsTeam,Insurancecompany,Paymentmethod,UserDetailsServicePrice,UserDetailsServicePackagePrice
from .models import UserDetailsSocialNetworks,UserDetailsFeatured,UserDetailsServicePackagePriceRemark,NewsletterMail
class SignUpAdmin(admin.ModelAdmin):
	list_display= ["__unicode__","timestamp","updated"]
	#form= SignUpForm
	#class Meta:
	#	model=SignUp
class UserDetailsAdmin(admin.ModelAdmin):
	list_display=["__unicode__","user"]
	#list_filter=["timestamp"]
	search_fields =["name"]
	class Meta:
		model=UserDetails

class UserDetailsServicePriceAdmin(admin.ModelAdmin):
	list_display = ("service", 'detail','detail_name')
	search_fields =["detail__surname"]	
	# za foreign key treba bit __ime(lookup)
	# u list_display detail_name je methoda na modelu
	# for reference list display admin to check online
	class Meta:
		model=UserDetailsServicePrice

admin.site.register(UserDetails,UserDetailsAdmin)
admin.site.register(UserDetailsRating)
admin.site.register(UserDetailsGallery)
admin.site.register(UserDetailsService)
admin.site.register(UserDetailsDepartment)
admin.site.register(UserDetailsTeam)
admin.site.register(Insurancecompany)
admin.site.register(Paymentmethod)
admin.site.register(UserDetailsServicePrice,UserDetailsServicePriceAdmin)
admin.site.register(UserDetailsServicePackagePrice)
admin.site.register(UserDetailsSocialNetworks)
admin.site.register(UserDetailsFeatured)
admin.site.register(UserDetailsServicePackagePriceRemark)
admin.site.register(NewsletterMail)