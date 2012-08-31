import json
import wowhead
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from worldofloot.main.models import Pin
from worldofloot.main.models import Item
from worldofloot.main.models import Image

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

def get_item_info(request, item_id):
  try:
    id = int(item_id)
  except:
    return HttpResponse(status=500)

  ret = 'exists'
  try:
    item = Item.objects.get(pk=id)
  except Item.DoesNotExist:
    pass
  print 'Grabbing info for item #', id
  ret = wowhead.scrape_item(id)

  response = {'images': []}
  for image in Image.objects.filter(item=item):
    response['images'].append(image.path)
  return HttpResponse(json.dumps(response), mimetype="application/json")


def add(request, item_id):
  return HttpResponse(status=200)

def vote_want(request):
  return HttpResponse(status=200)

def vote_have(request):
  return HttpResponse(status=200)

def add_item(request):
  return HttpResponse(status=200)

def remove_item(request):
  return HttpResponse(status=200)

