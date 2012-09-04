import json
import wowhead
import random
import string
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from worldofloot.main.models import UserProfile
from worldofloot.main.models import Pin
from worldofloot.main.models import Item
from worldofloot.main.models import Image

def index(request):
  return recent(request)

def recent(request):
  return render(request, 'main/index.html', {
    'tab': 'recent',

  })

def popular_gear(request):
  pins = Pin.objects.filter(item_type='gear').order_by('wants')
  return render(request, 'main/index.html', {
    pins: pins,

  })

def popular_mounts(request):
  pins = Pin.objects.filter(item_type='mount').order_by('wants')
  return render(request, 'main/index.html', {
    pins: pins,

  })

def my_loot(request):
  # get pins
  if 'anon_key' not in request.session:
    # we use our own session key because was having
    # problems accessing session.session_key before it was set.
    request.session['anon_key'] = random_string(20)

  print 'wtf', request.session['anon_key']

  if request.user.is_authenticated():
    pins = Pin.objects.filter(user=request.user)
  else:
    pins = Pin.objects.filter(session=request.session['anon_key'], user__isnull=True)

  items = []
  for pin in pins:
    item = pin.item
    images = item.image_set.order_by('priority')
    if len(images) > 0:
      item.image = images[0]
    items.append(item)

  print items
  return render(request, 'main/myloot.html', {
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


def add_item(request, item_type, item_id, verb):
  if verb not in ['want', 'have']:
    return HttpResponse('bad verb', status=500)

  try:
    id = int(item_id)
  except:
    return HttpResponse('bad id', status=500)

  try:
    item = Item.objects.get(item_id=id, item_type=item_type)
  except Item.DoesNotExist:
    print 'Serving 500 because we got an add request for an item not yet scraped'
    return HttpResponse(status=500)

  already_have = False
  increment_item_verb = False
  if request.user.is_authenticated():
    # logged in
    try:
      pin = Pin.objects.get(item=item, user=request.user)
      # check to make sure they didn't switch verb
      if pin.verb == verb:
        already_have = True
      else:
        # keep old wants and haves
        increment_item_verb = True
        pin.verb = verb
        pin.save()
    except Pin.DoesNotExist:
      pin = Pin(item=item, user=request.user)
      pin.save()
      increment_item_verb = True
  else:
    # TODO session expiration
    try:
      pin = Pin.objects.get(item=item, session=request.session['anon_key'])
      # check to make sure they didn't switch verb
      if pin.verb == verb:
        already_have = True
      else:
        # keep old wants and haves
        increment_item_verb = True
        pin.verb = verb
        pin.save()
    except Pin.DoesNotExist:
      pin = Pin(item=item, session=request.session['anon_key'])
      pin.save()
      increment_item_verb = True

  if increment_item_verb:
    if verb == 'want':
      item.wants += 1
    elif verb == 'have':
      item.haves += 1
    item.save()

  response = {'success': True, 'already_have': already_have}
  return HttpResponse(json.dumps(response), mimetype="application/json")

def remove_item(request, item_type, item_id):
  # doing this by item_id for now...maybe in the future take a pin id?
  try:
    id = int(item_id)
  except:
    return HttpResponse('bad id', status=500)

  item = Item.objects.get(item_id=item_id, item_type=item_type)
  if request.user.is_authenticated():
    Pin.objects.filter(user=request.user, item=item).delete()
  else:
    Pin.objects.filter(session=request.session['anon_key'], item=item).delete()

  return HttpResponse(status=200)

# TODO move this to its own app
# csrf reference, see https://docs.djangoproject.com/en/dev/ref/contrib/csrf/
# auth reference, see https://docs.djangoproject.com/en/dev/topics/auth/
def create_user(request):
  if 'username' not in request.POST or 'password' not in request.POST:
    return HttpResponse('bad request', status=500)
  username = request.POST['username']
  password = request.POST['password']

  user = authenticate(username=username, password=password)
  if user is None:
    # create the user, then log them in
    User.objects.create_user(username, '', password)
    user = authenticate(username=username, password=password)
    print 'User', username, 'created'
  return login_user(request, user)

def login_user(request, user):
    if user.is_active:
      login(request, user)
      print 'User', user.username, 'logged in'
      return HttpResponse(status=200)
    else:
      return HttpResponse('user deactivated', status=200)

def convert_session_to_user():
  pass

def random_string(n):
  return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(n))
