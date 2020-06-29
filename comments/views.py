from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.utils import timezone



from comments.models import Comment
from dataadd.models import Idiot
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from django.contrib import messages


def comment_delete(request, id ): #retrieve
	# for instanceAll in  Comment.objects.all():
	# 	print(instanceAll)
	#instance=get_object_or_404(Comment,id=id) #predajue parametar kod requesta
	try:
		instance=Comment.objects.get(id=id) #predajue parametar kod requesta
	except: 
		raise Http404
	
	if instance.user != request.user:
		response = HttpResponse("You do not have permission to view this")
		response.status_code=403
		return response

	postobj=instance.content_object
	if request.method=="POST":
		instance.delete()
		messages.success(request,"Deleted",extra_tags='some-tag')#
		return HttpResponseRedirect(postobj.get_absolute_url_comments())

	context={  
		"title":"Delete confirmation",
		"object":instance,
		"postobj":postobj,
		
	}
	#return HttpResponse ("<h1> helo3  </h1>")
	return render(request,"commentDelete.html",context)