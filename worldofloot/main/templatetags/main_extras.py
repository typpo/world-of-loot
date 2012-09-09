from django import template

register = template.Library()

@register.filter
def lookup(h, key):
  return h[key]
