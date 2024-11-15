from django.template import Library

register = Library()

@register.simple_tag
def is_active(request, url):
    return 'active' if request.path == url else ''