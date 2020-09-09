
from django.shortcuts import render
from django.views.generic import TemplateView 

# Create your views here.
def about(request):
	return render( request, "about.html",{})

class PrivacyPageView(TemplateView):
    template_name = "privacy.html"

def privacy(request):
	
	
	context={
		
		
	}

		
	
	return render(request,"privacy.html",context) #first page    