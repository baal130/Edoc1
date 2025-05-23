from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.urls import reverse





class CommentManager(models.Manager):  # Mijenjanje dafultnih modela npr Idiot.objects.all()
	def all(self):
		qs=super(CommentManager,self).filter(parent=None)
		return qs

	def filter_by_instance(self,instance):
		# content_type=ContentType.objects.get_for_model(Idiot)    #za dobivanje komentara
		content_type=ContentType.objects.get_for_model(instance.__class__)  #Instanca trazenog modela 
		obj_id=instance.id
		qs=super(CommentManager,self).filter(content_type=content_type,object_id= obj_id).filter(parent=None)
		return qs


class Comment(models.Model):
	user	 =models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE,)
	#post	 =models.ForeignKey(Idiot)
	content  =models.TextField()
	timestamp=models.DateTimeField(auto_now_add=True)

	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	parent=models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE,)

	objects=CommentManager() # means objects are modeled trough manager  super(CommentManager,self)=comments.objects
	class Meta:
		ordering=['-timestamp']
		
	def get_absolute_url_delete(self):
		#return "/complain/%s/" %(self.id)
		return reverse("comments:comment_delete", kwargs={"id":self.id})			
	def get_rating_from_user(self):
		user=self.user	
		rate =user.userdetailsrating_set.first().rating
		if rate is None:
			rate=5.0
		
		return rate
	def get_usercommented_from_user(self):
		user=self.user	
		userdetail =user.userdetailsrating_set.first().detail
		return userdetail
	def __unicode__(self):
		return str(self.user.username)
	def __str__(self):
		return str(self.user.username)
	def children(self): #replies
		return Comment.objects.filter(parent=self)
	@property
	def is_parent(self):
		if self.parent is not None:
			return False
		return True
	