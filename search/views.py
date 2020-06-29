from django.views.generic import View
from django.shortcuts import render
from .utils import yelp_search
# Create your views here.


class SearchView(View):
    def get(self, request, *args, **kwargs):
        items = []
        q = request.GET.get('q')
        loc = request.GET.get('loc')
        lat=request.GET.get('lat')
        print(request.GET)
        print(lat)
        lng=request.GET.get('lng')
        if not lat:
            # tu treba od user sessiana
            lat=11.6971494
            lng=-75.2598644
        else:   
            lat=request.GET.get('lat')
            lng=request.GET.get('lng')
        print(lat)
        print(lng)
        # ako nema loc i q treba stavit
        if not q:
            q='doctor'
        if not loc:
            location = request.session.get('CITY', 'Newport Beach')
            print(location)
        else:
            location = loc
        
        items = yelp_search(keyword=q, location=location,lat=lat,lng=lng,) 
            
        return render(request, 'search/home.html', {'results': items})

        return render(request, 'search/home.html', {'results': items})