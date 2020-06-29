from django.contrib import admin

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
	list_display=["user","timestamp"]
	list_filter=["timestamp"]
	search_fields =["user"]
	class Meta:
		model=Comment


admin.site.register(Comment)