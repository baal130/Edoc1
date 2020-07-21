from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.utils import timezone


from .models import Idiot,Friends,FriendsRequests #za query import // CUSTOM FRIENDS

from newsletter.models import UserDetails
from .forms import IdiotForm,CategoryForm,NewsForm
# from django.contrib.auth.models import User

from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from django.views.generic import CreateView, DetailView, View
from django.contrib.auth import get_user_model
from django.utils import translation 
from django.utils.translation import gettext_lazy as _
from el_pagination.views import AjaxListView
from el_pagination.decorators import page_template

User = get_user_model()

from .utils import get_read_time



class ProfileFollowToggle(View):
	def post(self, request, *args, **kwargs):
		username_to_toggle = request.POST.get("username")
		slug = request.POST.get("slug")
		instance=get_object_or_404(Idiot,slug=slug) #da bi se znao vratiti na isti post od UserDetails
		
		profile_, is_following = UserDetails.objects.toggle_follow(request.user, username_to_toggle)
		return HttpResponseRedirect(instance.get_absolute_url())
class ProfileFollowToggleList(View):
	def post(self, request, *args, **kwargs):
		username_to_toggle = request.POST.get("username")
		
		
		profile_, is_following = UserDetails.objects.toggle_follow(request.user, username_to_toggle)
		return redirect("/complain/friends/")		  

def doctor_article_detail(request, slug): #retrieve
	
	instance=get_object_or_404(Idiot,slug=slug) #predajue parametar kod requesta
	
	## with normal way get comment 
	# content_type=ContentType.objects.get_for_model(Idiot)    #za dobivanje komentara
	# obj_id=instance.id
	# comments=Comment.objects.filter(content_type=content_type,object_id= obj_id)
	
	

	initial_data={
		"content_type":instance.get_content_type,
		"object_id":instance.id,
	}
	## trough model manager  
	comment_form=CommentForm(request.POST or None,initial=initial_data)
	if comment_form.is_valid():
		c_type=comment_form.cleaned_data.get("content_type")
		content_type=ContentType.objects.get(model=c_type)
		obj_id=comment_form.cleaned_data.get("object_id")
		parent_obj=None
		try:
			parent_id=int(request.POST.get("parent_id"))
		except:
			parent_id=None
		if parent_id:
			parent_qs=Comment.objects.filter(id=parent_id)
			if parent_qs.exists():
				parent_obj=parent_qs.first()


		content_data=comment_form.cleaned_data.get("content")
		new_comment,created =Comment.objects.get_or_create(
							user=request.user,
							content_type=content_type,
							object_id=obj_id,
							content=content_data,
							parent=parent_obj,
						)
		print(new_comment.content_object.get_absolute_url())
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())  
	#comments=Comment.objects.filter_by_instance(instance) #by query set and model manager in Comment model
	comments=instance.comments    # by property in Idiot model class
	instanceUser=UserDetails.objects.get(user=instance.user)#user od posta 
	is_following = False
	if request.user.is_authenticated:
		if instanceUser in request.user.is_following.all(): #ako je user od posta prati od ovog koji je registriarn
			is_following = True
	
	otherarticles=Idiot.objects.filter(user=instance.user)
	print(otherarticles)
	otherarticles=otherarticles.exclude(company_name=instance.company_name)
	print(otherarticles)
	context={  
		"title":"Punch Detail",
		"instance":instance,
		"comments":comments,
		"comment_form":comment_form,
		"is_following":is_following,
		"slug":slug,
		"otherarticles":otherarticles,
	}
	
	return render(request,"detail_article.html",context)
def doctor_article_create(request):
	if not request.user.is_authenticated:
		raise Http404
		
	# if 'lang' in request.GET:
	# 	translation.activate(request.GET.get('lang'))
	# 	translation.activate('es')
	# user_language = 'es'
	# translation.activate(user_language)
	# request.session[translation.LANGUAGE_SESSION_KEY] = user_language
	# print(request.GET.get('lang'))	
	# print(translation.activate(request.GET.get('lang')))	
	user_detail_instance=UserDetails.objects.filter(user=request.user) #  ako je vec popunio  tada dopusti da kreira post
	if user_detail_instance.exists():
		user_detail_instance=UserDetails.objects.get(user=request.user)
		if user_detail_instance.verificated is  True:    # ako je verificarian dopusti mu napisati post 
			print(user_detail_instance.name)
		

			userdatafilled=True
		
		
			title = _('ADD ARTICLE')
			if  request.user.is_staff or request.user.is_superuser:
				 form=NewsForm(request.POST or None, request.FILES or None)# za admine omoguceno pisanje newsa
			else:     
				form=IdiotForm(request.POST or None, request.FILES or None)# za file foldere
			if form.is_valid(): 
				instance=form.save(commit=False)
				instance.user=request.user
				instance.save()
				#print instance.image.url
				messages.success(request,"Success",extra_tags='some-tag')#
				return HttpResponseRedirect(instance.get_absolute_url())
			if form.errors:
				print(form.errors)
				messages.error(request,"Not Success")
			
			context={
			  "form1":form,
			  "title":title,
			  "user_detail_instance":user_detail_instance,
			  "userdatafilled":userdatafilled,
			  #"time": instance.timestamp,
			}
		else:#    Verification else ( wait for verification )
			
			
			title =('Please wait until Your account is verificated')
			context={
			"title":title,
			
			
			} 

				 
	else:
		title=_('Fill your profile')
		userdatafilled=False
		context={
		"title":title,
		"userdatafilled":userdatafilled,
		}

	return render(request,"complain.html",context)
	#return HttpResponse ("<h1> helo144 </h1>")

def doctor_article_list (request): #list items
	#queryset_list=Idiot.objects.filter(draft=False).filter(publish__lte=timezone.now())#all()  #lte means l then or equal pusblish is model field ovo se koristi normalno

	category_form=CategoryForm(request.POST or None)
	
	queryset_list=Idiot.objects.active().filter(article=False)   #filter je napravljen u modelima i instaciran 
	

	if  request.user.is_staff or request.user.is_superuser: 
		queryset_list=Idiot.objects.all()
	query=request.GET.get("q")
	nametest=request.GET.get("color")
	


	if query:
		queryset_list=queryset_list.filter(
			Q(company_name__icontains=query)|
			Q(description__icontains=query)
			#Q(user__first_name__icontains=query) |
			#Q(user__last_name__icontains=query)
				).distinct()
	if(nametest):
		
		queryset_list=queryset_list.filter(
			Q(cities__icontains=nametest)
		  ).distinct()
				
	   
	paginator = Paginator(queryset_list, 4) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	context={
		# "object_list":queryset_list,
		"object_list":queryset,
		"title":"List",
		"page_request_var":page_request_var,
		"category":category_form,
	}      
	
	return render(request,"article_list.html",context)
	#return HttpResponse ("<h1> helo14454252</h1>")
def doctor_article_update (request, slug): #update
	instance=get_object_or_404(Idiot, slug=slug)
	if instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404

	form=IdiotForm(request.POST or None,request.FILES or None,instance=instance)
	if form.is_valid():
		instance=form.save(commit=False)
		#print form.cleaned_data.get("company_name")
		instance.save()
		messages.success(request,"Saved")
		return HttpResponseRedirect(instance.get_absolute_url())
	userdatafilled=True
	context={
	  "instance":instance,
	  "form1":form,
	  "title":instance.company_name,
	  "userdatafilled":userdatafilled,
	}           
	return render(request,"complain.html",context)
def doctor_article_delete (request,slug=None): #delete
	instance=get_object_or_404(Idiot, slug=slug)
	
	instance.delete()
	
	messages.success(request,instance.company_name)
	messages.success(request,"Deleted")

	return redirect("dataadd:complain_list")

def myarticle(request):
	queryset_list=Idiot.objects.filter(user=request.user)  #filter je napravljen u modelima i instaciran 
	# if  request.user.is_staff or request.user.is_superuser: 
	#   queryset_list=Idiot.objects.all()
	query=request.GET.get("q")
	if query:
		queryset_list=queryset_list.filter(
			Q(company_name__icontains=query)|
			Q(description__icontains=query)
			#Q(user__first_name__icontains=query) |
			#Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 4) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	context={
		"object_list":queryset,
		"title":"List",
		"page_request_var":page_request_var,
	}      

	return render(request,"my_article_list.html",context)

def article(request):
	category_form=CategoryForm(request.POST or None)
	
	queryset_list=Idiot.objects.active().filter(article=True)   #filter je napravljen u modelima i instaciran 
	

	if  request.user.is_staff or request.user.is_superuser: 
		queryset_list=Idiot.objects.all()
	query=request.GET.get("q")
	nametest=request.GET.get("color")
	


	if query:
		queryset_list=queryset_list.filter(
			Q(company_name__icontains=query)|
			Q(description__icontains=query)
			#Q(user__first_name__icontains=query) |
			#Q(user__last_name__icontains=query)
				).distinct()
	if(nametest):
		
		queryset_list=queryset_list.filter(
			Q(cities__icontains=nametest)
		  ).distinct()
				
	   
	paginator = Paginator(queryset_list, 4) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	context={
		"object_list":queryset,
		"title":"List",
		"page_request_var":page_request_var,
		"category":category_form,
	}   

	return render(request,"article_list.html",context)   
def friends(request):
	title='ggf'
	user=User.objects.first()
	users=User.objects.exclude(id=request.user.id) #svi useri osim logiranog
	# friend=Friends.objects.get(current_user=request.user)  #dohvati objekt Frienda
	friend=UserDetails.objects.get(user=request.user)  #dohvati objekt Frienda
	#friends2=user.friends_set.all()
	#friend_rev=friends2.objects.get(user=request.user)
	# friends=friend.users.all() #izlistaj usere u objektu Friend
	followers=friend.followers.all() #izlistaj usere u objektu Friend
	following=request.user.is_following.all()
	# try:
	# friendrequest=FriendsRequests.objects.get(current_user=request.user)
	# # except:
	# #     friendrequest=FriendsRequests()
	# #     friendrequest.save()   

	# friendsrequests=friendrequest.usersRequests.all() #izlistaj usere u objektu Friend.all() #izlistaj usere u objektu Friend
	# friendsrequestssent=friendrequest.usersRequestsSent.all()

	query=request.GET.get("q")
	
	


	if query:
		users=users.filter(
			Q(username__icontains=query)|
			Q(last_name__icontains=query)
			#Q(user__first_name__icontains=query) |
			#Q(user__last_name__icontains=query)
				).distinct()



	followingTrue=True
	followingFalse=False
	context={"title":title,
	   "followers":followers,
	   "users":users, 
	   "following":following,  
	   "followingTrue":followingTrue,
	   "followingFalse":followingFalse,
	   # "friendsrequests":friendsrequests,
	   # "friendsrequestssent":friendsrequestssent,
	  #  "friend_rev":friend_rev,
	}
	return render(request,"friends_list.html",context)



def connect(request,operation,pk):
	new_friend=User.objects.get(pk=pk)
	if operation =='add':
		Friends.make_friend(request.user,new_friend)
		FriendsRequests.del_friendreq(new_friend,request.user)   


	elif operation == 'remove':
		Friends.del_friend(request.user,new_friend)    
	return redirect("dataadd:friends")    

def connectrequest(request,operation,pk):   #friendship request 
	new_friend=User.objects.get(pk=pk)
	if operation =='add':
		FriendsRequests.make_friendreq(request.user,new_friend)
		


	elif operation == 'remove':
		FriendsRequests.del_friendreq(request.user,new_friend)    
	return redirect("dataadd:friends")     
def entry_index(request, template='test_pag.html'):
	context = {
		'entry_list': Idiot.objects.all(),
	}
	return render(request, template, context)	
@page_template('service_list_pag.html')  # just add this decorator gdje se prikazuju svi rezultati 
def entry_list(request,template=None, extra_context=None): 
	context = {
		'entry_list': Idiot.objects.all(),
	}
   
	if extra_context is not None:
		context.update(extra_context)
	print(template)
	
	return render(request, template, context)    