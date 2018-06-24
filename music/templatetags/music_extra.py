from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='replaceChar')
@stringfilter
def replaceChar(string,char_to_replace,replacment_char=" "):
    return string.replace(char_to_replace,replacment_char)

