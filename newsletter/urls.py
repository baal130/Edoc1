from django.conf.urls import include,url
from django.contrib import admin
from el_pagination.decorators import page_template, page_templates
from .views import (
	discount_detail,
	discount_list,
	doctor_list,
	DetailRatingAjaxView,
	delete_galery,
	delete_service,
	delete_team,
	delete_department,
	entry_list,
	user_detail_package_update,
	package_delete,
	language_delete,
	
)

app_name = 'newsletter'
urlpatterns =[
	url(r'^ajax/rating/$',DetailRatingAjaxView.as_view(), name='ajax_rating'),# mora ic prvo, tu se salje post od ajaxa u detaildoctor.html
	# url(r'^(?P<slug>[\w-]+)/$',page_template('service_list_pag.html')(entry_list),#page template se zove s {% include page_template %}
	# 	                       {'template': 'index-singlepage.html'}, 
 #        						name='doctor_detail'),
	url(r'packagedelete/(?P<pk>\d+)/$',package_delete,name='package_delete'),
	url(r'delete/(?P<pk>\d+)/$',delete_galery,name='delete_galery'),
	url(r'deleteservice/(?P<pk>\d+)/$',delete_service,name='delete_service'),
	url(r'deleteteam/(?P<pk>\d+)/$',delete_team,name='delete_team'),
	url(r'deletedepartment/(?P<pk>\d+)/$',delete_department,name='delete_department'),
	url(r'deletelanguage/(?P<pk>\d+)/$',language_delete,name='language_delete'),
	url(r'packageupdate/(?P<pk>\d+)/$',user_detail_package_update,name='user_detail_package_update'),
	url(r'packages/(?P<slug>[\w-]+)/$',page_templates({
           
            
        })(discount_detail),{'template': 'discount_detail.html'},  name='discount_detail'),
	
	url(r'^discounts/$',page_templates({
            
            'discount_package_list_pag.html': 'dis-package-page',
        })(discount_list),{'template': 'discount_list.html'},  name='discount_list'),


	url(r'^(?P<slug>[\w-]+)/$',page_templates({
            'service_list_pag.html': 'service-page',
            'complain_list_pag1.html': 'test-page',
            'price_list_pag.html': 'price-page',
            'package_list_pag.html': 'package-page',
        })(entry_list),{'template': 'index-singlepage.html'},  name='doctor_detail'),
	url(r'^(?P<slug>[\w-]+)/comments/$',page_templates({
            'service_list_pag.html': 'service-page',
            'complain_list_pag1.html': 'test-page',
            'price_list_pag.html': 'price-page',
            'package_list_pag.html': 'package-page',
        })(entry_list),{'template': 'index-comments.html'},  name='comments'),

	url(r'$',doctor_list, name='doctor_list'),
	
	
	

	
	
]
