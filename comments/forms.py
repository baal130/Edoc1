from django import forms

from django.utils.translation import ugettext_lazy as _


class CommentForm(forms.Form):  #
	content_type=forms.CharField(widget=forms.HiddenInput)
	object_id=forms.IntegerField(widget=forms.HiddenInput)
	parent_id=forms.IntegerField(widget=forms.HiddenInput,required=False)
	content=forms.CharField(widget=forms.Textarea, label="Comment")
	