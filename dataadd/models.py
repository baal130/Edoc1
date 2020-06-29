from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from datetime import date
from django.utils import timezone
from markdown_deux import markdown
from ckeditor.fields import RichTextField

from comments.models import Comment 
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from .utils import get_read_time


class PostManager(models.Manager):  # Mijenjanje dafultnih modela npr Idiot.objects.all()
	def active(self, *args, **kwargs):
		return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())

def uplodad_location(instance, filename):
	return "%s/%s" %(instance.id,filename)

CITY_CHOICES = (
	('', '----'),
	('Bjelovarsko-bilogorska','BJELOVARSKO-BILOGORSKA'),
	('Brodsko-posavska', 'BRODSKO-POSAVSKA'),
	('Dubrovacko-neretvanska','DUBROVACKO-NERETVANSKA'),
	('Istarska','ISTARSKA'),
	('Karlovacka','KARLOVACKA'),
)

class Friends(models.Model):
	users=models.ManyToManyField(User,related_name='sender')#related name koristi many to many to many field dafultno je ime classe_set
	current_user=models.ForeignKey(User,related_name='owner',null=True,on_delete=models.CASCADE)
	
	@classmethod
	def make_friend(cls,current_user,new_friend):    # svaki user ce imati svoju listu friendova i kreiraju se dva objekta
		friend,created = cls.objects.get_or_create(    #cls je vec klasa sama (Friend)
			current_user=current_user
		)
		friendother,created =cls.objects.get_or_create( 
			current_user=new_friend
		)
		friend.users.add(new_friend)
		friendother.users.add(current_user)
	@classmethod
	def del_friend(cls,current_user,new_friend):
		friend,created = cls.objects.get_or_create(
			current_user=current_user
		)
		friendother,created =cls.objects.get_or_create( 
			current_user=new_friend
		)
		friend.users.remove(new_friend)	
		friendother.users.remove(current_user)
class FriendsRequests(models.Model):
	usersRequests=models.ManyToManyField(User,related_name='senderrequests')#koje requestove ima current user 
	usersRequestsSent=models.ManyToManyField(User,related_name='senderrequestssent') #kome je current user poslao request
	current_user=models.ForeignKey(User,related_name='ownerrequest',null=True,on_delete=models.CASCADE)

	@classmethod
	def make_friendreq(cls,current_user,new_friend):    # svaki user ce imati svoju listu friend req i kreiraju se dva objekta
		friendreq,created = cls.objects.get_or_create(    #cls je vec klasa sama (Friend), u bazi od usere se cuvaju gdje je poslan request
			current_user=current_user
		)
		friendotherreq,created =cls.objects.get_or_create( #u bazi od od drugog usera( gdje je poslan request) se cuvaju gdje je otkuda je dosao request
			current_user=new_friend
		)
		friendreq.usersRequestsSent.add(new_friend)
		friendotherreq.usersRequests.add(current_user)
	@classmethod
	def del_friendreq(cls,current_user,new_friend):
		friendreq,created = cls.objects.get_or_create(
			current_user=current_user
		)
		friendotherreq,created =cls.objects.get_or_create( 
			current_user=new_friend
		)
		friendreq.usersRequestsSent.remove(new_friend)
		friendotherreq.usersRequests.remove(current_user)
class Idiot(models.Model): 
	# punch list articels 
	user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
	company_name = models.CharField(max_length=120,blank=False,null=False) #blank=false kada je potrebno unijeti polje
	slug=models.SlugField(unique=True)
	description =  models.TextField(max_length=400,blank=False,null=False)
	#image =models.FileField(null=True,blank=True)
	image =models.ImageField(upload_to=uplodad_location, # upload_to=images/
		null=True,
		blank=True,
		width_field="width_field",
		height_field="height_field")
	width_field=models.IntegerField(default=0)
	height_field=models.IntegerField(default=0)
	draft=models.BooleanField(default=False)
	name=models.CharField(max_length=60,blank=False,null=False,default='a')
	surname=models.CharField(max_length=60,blank=False,null=False,default='a')
	adress=models.CharField(max_length=60,blank=False,null=False,default='a')
	city=models.CharField(max_length=60,blank=False,null=False,default='a')
	publish= models.DateField(auto_now=False, auto_now_add=False,default=date.today)
	read_time=models.TimeField(null=True,blank=True)
	name_visible=models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
	updated = models.DateTimeField(auto_now_add=False,auto_now=True)
	article=models.BooleanField(default=False) # true if used for article 
	news=models.BooleanField(default=False) # true if used for news(only for admin)
	cities = models.CharField(max_length=40,choices=CITY_CHOICES,
				 default='null',blank=True)

 
	objects=PostManager()

	def __unicode__(self):
		return self.company_name #ono sto se vidi u databasa kad gledamo ( u adminu npr)
	def get_absolute_url(self):
		#return "/complain/%s/" %(self.id)
		#return reverse("dataadd:detail", kwargs={"id":self.id}) Za dynamicno prikazivanje urla
		return reverse("dataadd:detail", kwargs={"slug":self.slug}) # Za dynamicno prikazivanje urla
		
	def get_absolute_url_delete(self):
		#return "/complain/%s/" %(self.id)
		return reverse("dataadd:delete", kwargs={"slug":self.slug})	

	class Meta:
		ordering =["-timestamp","-updated"]	
	
	def get_markdown(self):
		content=self.description
		# return mark_safe(markdown(content)) for pagedown is ok
		return mark_safe(content) # for sumernote content already html
	def get_user(self):
		article_user=self.user
		print(user.profilepicture.url)
		return self.user	
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
	@property 
	def commentscount(self):
		instance=self
		qs=Comment.objects.filter_by_instance(instance)
		count=qs.count()
		return count		

def create_slug(instance, new_slug=None):
	slug=slugify(instance.company_name)
	if new_slug is not None:
		slug=new_slug
	qs=Idiot.objects.filter(slug=slug).order_by("-id")
	exists=qs.exists()
	if exists:
		new_slug= "%s-%s" %(slug,qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug
def pre_save_complain_receiver(sender,instance, *args, **kwargs):
	# slug=slugify(instance.company_name)
	# exists=Idiot.objects.filter(slug=slug).exists()
	# if exists:
	# 	slug ="%s-%s" %(slug,instance.id)
	# instance.slug=slug
	if not instance.slug:
		instance.slug =create_slug(instance)	
	if instance.description:
		html_string=instance.get_markdown()
		read_time_var=get_read_time(html_string)
		instance.read_time=read_time_var
		
pre_save.connect(pre_save_complain_receiver, sender=Idiot)