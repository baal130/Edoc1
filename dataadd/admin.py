from django.contrib import admin

from .models import Idiot,Friends


class IdiotAdmin(admin.ModelAdmin):
	list_display=["company_name","timestamp"]
	list_filter=["timestamp"]
	search_fields =["company_name"]
	class Meta:
		model=Idiot


admin.site.register(Idiot, IdiotAdmin)
admin.site.register(Friends)