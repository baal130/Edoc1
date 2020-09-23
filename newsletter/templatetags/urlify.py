from urllib.parse import quote
from django import template

register=template.Library()

@register.filter  #simple tag use it as  example {{instance.adress|urlify}} and before {% load urlify%}
def urlify(value):
	return quote(value)
