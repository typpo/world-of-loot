import urllib2
import re
from xml.etree.ElementTree import parse
from worldofloot.main.models import Item
from worldofloot.main.models import Image

def scrape_item(id, item_type):
  html = urllib2.urlopen('http://www.wowhead.com/%s=%d'
      % (item_type, id)).read()
  if item_type == 'item':
    # an actual piece of gear
    xml = parse(urllib2.urlopen('http://www.wowhead.com/%s=%d?xml'
      % (item_type, id)))

    name = xml.find('item/name').text
    ilvl = int(xml.find('item/level').text)
    quality = xml.find('item/quality').text
    icon = xml.find('item/icon').text
    slot = xml.find('item/inventorySlot').text

    print name, ilvl, quality, icon, slot
    item = Item(item_id=id, item_type=item_type, name=name,
        ilvl=ilvl, quality=quality, icon=icon, slot=slot)
    print slot, quality
    #item.tags.add(slot, quality)
  else:
    # a mount or spell or set
    name_regex = re.compile('\<meta property="og:title" content="(.*?)" /\>')
    m = name_regex.search(html)
    name = m.group(1)
    print 'Non-item', name, item_type
    item = Item(item_id=id, item_type=item_type, name=name)
    #item.tags.add(item_type)

  # commit to db
  item.save()

  # now look for images
  # TODO for items that don't have images, we should check for images
  # every now and then because they could've been added.
  image_regex = re.compile("{id:(\d+),user:'(.*?)'(.*?)}")
  image_count = 0
  #images = []
  print item_type, id
  for m in image_regex.finditer(html):
    image_id = m.group(1)
    attribution = m.group(2)
    image_count += 1

    path = 'http://wow.zamimg.com/uploads/screenshots/normal/%s.jpg' % image_id
    thumb_path = 'http://wow.zamimg.com/uploads/screenshots/thumb/%s.jpg' % image_id
    # sticky:1 indicates best image
    print '\tImage:', image_id, 'by', attribution

    new_image = Image.objects.create(item=item, image_id=image_id, path=path,
        thumb_path=thumb_path, attribution=attribution)

    if m.group(3).endswith('sticky:1'):
      new_image.priority = 0
      new_image.resize()   # resize and upload to s3
    else:
      new_image.priority = image_count
    #images.append(new_image)

  #Image.objects.bulk_create(images)

  return item
