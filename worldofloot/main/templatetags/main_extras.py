from django import template

register = template.Library()

@register.filter
def lookup(h, key):
  return h[key]

@register.filter
def toThumb(img_src):
  return img_src.replace('normal', 'thumb')
