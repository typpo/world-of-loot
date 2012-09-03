import sys
import re
import string
from redis_completion import RedisEngine

CRAWL_DATA_PATH = 'data/all'
engine = RedisEngine(prefix='worldofloot:autocomplete')

def strip_punctuation(s):
  return re.sub(ur"\p{P}+", "", s)

def canonicalize_input(s):
  return strip_punctuation(s.lower())

def create():
  print 'Flushing old...'
  engine.flush()
  print 'Creating...'
  regex = re.compile('wowhead.com/(item|spell|itemset|transmog-set)=(.*?)/(.*?)<')
  c = 0
  itemname_set = set()
  dict_lookup = {}
  for line in open(CRAWL_DATA_PATH):
    m = regex.search(line)
    if m and len(m.groups()) == 3:
      c += 1
      item_id = m.group(2)
      item_name = m.group(3).replace('-', ' ')
      item_type = m.group(1)
      canonicalized_name = canonicalize_input(m.group(3).replace('-', ' '))

      engine.store_json(item_id, item_name, {
        'name': item_name,
        'id': item_id,
        'type': item_type,
      })
  print 'Done.'

def search(q):
  # TODO dedup and pick by highest id
  return engine.search_json(canonicalize_input(q))

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
