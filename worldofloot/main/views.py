from django.shortcuts import render_to_response
from worldofloot.main.models import Pin

def index(request):
  return recent()

def recent(request):
  return render_to_response('main/index.html', {

  })

def popular_gear(request):
  pins = Pin.objects.filter(item_type='gear').order_by('wants')
  return render_to_response('main/index.html', {
    pins: pins,

  })

def popular_mounts(request):
  pins = Pin.objects.filter(item_type='mount').order_by('wants')
  return render_to_response('main/index.html', {
    pins: pins,

  })

def my_loot(request):
  return render_to_response('main/myloot.html', {

  })

def vote_want(request):
  pass

def vote_have(request):
  pass

def add_item(request):
  pass

def remove_item(request):
  pass
