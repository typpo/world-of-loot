import json
import wowhead
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from worldofloot.main.models import Pin
from worldofloot.main.models import Item
from worldofloot.main.models import Image

def index(request):
  return recent(request)

def recent(request):
  return render_to_response('main/index.html', {
    'tab': 'recent',

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
  # get pins
  if request.user.is_authenticated():
    # TODO
    return HttpResponse('you be authed')
  else:
    """
    if 'pins' not in request.session:
      request.session['pins'] = []
    pins = request.session['pins']
    """
    pins = Pin.objects.filter(session=request.session.session_key)

  items = []
  for pin in pins:
    item = pin.item
    images = item.image_set.order_by('priority')
    if len(images) > 0:
      item.image = images[0]
    items.append(item)

  print items
  return render_to_response('main/myloot.html', {
    'items': items,
    'tab': 'my_loot',

  })

def get_item_info(request, item_type, item_id):
  try:
    id = int(item_id)
  except:
    return HttpResponse(status=500)

  try:
    item = Item.objects.get(item_id=id, item_type=item_type)
    print 'Item #', id, 'already exists in database'
  except Item.DoesNotExist:
    print 'Grabbing info for item #', id
    item = wowhead.scrape_item(id, item_type)

  response = {'success': True, 'images': [], 'name': item.name}
  for image in Image.objects.filter(item=item).order_by('priority'):
    response['images'].append(image.path)

  return HttpResponse(json.dumps(response), mimetype="application/json")


def add_item(request, item_type, item_id):
  try:
    id = int(item_id)
  except:
    return HttpResponse('bad id', status=500)

  try:
    item = Item.objects.get(item_id=id, item_type=item_type)
    item.wants += 1
    item.save()
  except Item.DoesNotExist:
    print 'Serving 500 because we got an add request for an item not yet scraped'
    return HttpResponse(status=500)

  if request.user.is_authenticated():
    # logged in
    # TODO
    pass
  else:
    # TODO session expiration
    pin = Pin(item=item, session=request.session.session_key)
    pin.save()
    print 'Saved an anonymous pin'

  response = {'success': True}
  return HttpResponse(json.dumps(response), mimetype="application/json")

def remove_item(request, item_type, item_id):
  # doing this by item_id for now...maybe in the future take a pin id?
  try:
    id = int(item_id)
  except:
    return HttpResponse(status=500)


  if request.user.is_authenticated():
    # TODO
    pass
  else:
    item = Item.objects.get(item_id=item_id, item_type=item_type)
    Pin.objects.filter(session=request.session.session_key, item=item).delete()

  return HttpResponse(status=200)

def vote_want(request):
  return HttpResponse(status=200)

def vote_have(request):
  return HttpResponse(status=200)

def convert_session_to_user():
  pass
