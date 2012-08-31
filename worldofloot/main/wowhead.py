import urllib2
import re
from xml.etree.ElementTree import parse
from worldofloot.main.models import Item
from worldofloot.main.models import Image

def scrape_item(id):
  xml = parse(urllib2.urlopen('http://www.wowhead.com/item=%d?xml' % id))

  name = xml.find('item/name').text
  ilvl = int(xml.find('item/level').text)
  quality = xml.find('item/quality').text
  icon = xml.find('item/icon').text
  slot = xml.find('item/inventorySlot').text

  html = urllib2.urlopen('http://www.wowhead.com/item=%d' % id).read()
  image_regex = re.compile("id:(\d+),user:'(.*?)'")

  print name, ilvl, quality, icon, slot
  item = Item(item_id=id, item_type='gear', name=name,
      ilvl=ilvl, quality=quality, icon=icon, slot=slot)
  item.save()

  image_count = 0
  for m in image_regex.finditer(html):
    image_id = m.group(1)
    attribution = m.group(2)
    image_count += 1

    path = 'http://wow.zamimg.com/uploads/screenshots/normal/%s.jpg' % image_id
    thumb_path = 'http://wow.zamimg.com/uploads/screenshots/thumb/%s.jpg' % image_id

    print '\tImage:', image_id, 'by', attribution

    image = Image(item=item, image_id=image_id, path=path,
        thumb_path=thumb_path, attribution=attribution)
    image.save()

  return item
