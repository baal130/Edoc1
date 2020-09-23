from django import template
from dataadd.models import Idiot

register = template.Library()
#used in footer section , need to be added also in settings 
@register.simple_tag
def get_article_list(max_results=0):
    queryset = Idiot.objects.all()
    if max_results == 0:
        return queryset
    elif max_results > 0:
        return queryset[:min(max_results, queryset.count())]
    else:
        return None