import sys
import re
import string
import os
from redis_completion import RedisEngine

CRAWL_DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/all')
engine = RedisEngine(prefix='worldofloot:autocomplete', db=2)

def strip_punctuation(s):
  return re.sub(ur"\p{P}+", "", s)

def canonicalize_input(s):
  return strip_punctuation(s.lower())

def create():
  print 'Flushing old...'
  engine.flush()
  print 'Creating...'
  #regex = re.compile('wowhead.com/(item|spell|itemset|transmog-set)=(.*?)/(.*?)<')
  regex = re.compile('wowhead.com/(item|spell|itemset|transmog-set)=(.*?)/(.*?)</loc>(<priority>(.*?)<)?')
  c = 0
  itemname_set = set()
  dict_lookup = {}
  for line in open(CRAWL_DATA_PATH):
    m = regex.search(line)
    if m and len(m.groups()) > 2:
      c += 1
      item_id = m.group(2)
      item_name = m.group(3).replace('-', ' ')
      item_type = m.group(1)
      if len(m.groups()) > 4 and m.group(5):
        priority = float(m.group(5))
      else:
        priority = 0
      canonicalized_name = canonicalize_input(m.group(3).replace('-', ' '))

      # TODO some are getting overwritten - order matters!

      engine.store_json(item_id, canonicalized_name, {
        'name': item_name,
        'id': item_id,
        'type': item_type,
        'priority': priority
      })
    else:
      print 'Failed on line', line
  print 'Added', c
  print 'Done.'

def search(q):
  # Dedup items by name in a way that will hopefully increase
  # the likelihood that an image is available.
  # TODO move some of this to preprocessing
  results = engine.search_json(canonicalize_input(q))
  return sorted(results, key=lambda k: k['priority'], reverse=True)

  """
  results_by_name = {}
  # group results by name
  for result in results:
    name = result['name']
    # reject bad items
    # TODO make this neater
    # TODO or name contains number
    if name.find('test') > -1 or name.endswith('visual') \
      or name.find('summon') > -1 or name.startswith('put up') \
      or name.endswith('aura') or name.startswith('monster') \
      or name.startswith('flight path') or name.startswith('copy') \
      or name.endswith('old') or name.find('effect') > -1 \
      or name.find('portal') > -1 or name.startswith('create') \
      or name.startswith('aggro') or name.endswith('credit') \
      or name.endswith('cosmetic') or name.startswith('remove') \
      or name.find('dnd') > -1 or name.endswith('spawn') \
      or name.find('teleport') > -1 or name.startswith('camera'):
      continue
    results_by_name.setdefault(name, [])
    results_by_name[name].append(result)

  # then dedup
  final_results = []
  for name, results in results_by_name.iteritems():
    # prefer items over spells
    items = []
    results_for_this_name = results
    for result in results:
      if result['type'] == 'item':
        items.append(result)
    if len(items) > 0:
      # only choose from just items
      results_for_this_name = items

    # now choose the highest id, because that seems to be the aggregator
    if len(results_for_this_name) > 0:
      new_results = sorted(results_for_this_name,
          key=lambda k: k['id'], reverse=True)
      final_results.append(new_results[0])

  return final_results
  """

if __name__ == '__main__':
  if len(sys.argv) > 1 and sys.argv[1] == 'create':
    create()
  while True:
    q = raw_input('? ')
    if q == 'q':
      break
    results = search(q)
    for result in results:
      print result
