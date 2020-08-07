from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



from .models import GuestEmail, EmailActivation

User = get_user_model()





# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)



class EmailActivationAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model = EmailActivation


admin.site.register(EmailActivation, EmailActivationAdmin)


class GuestEmailAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model = GuestEmail


admin.site.register(GuestEmail, GuestEmailAdmin)