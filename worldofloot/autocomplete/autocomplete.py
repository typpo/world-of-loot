import sys
import re
import string
from redis_completion import RedisEngine

CRAWL_DATA_PATH = 'data/all'
engine = RedisEngine(prefix='worldofloot:autocomplete')

def strip_punctuation(s):
  return s.translate(string.maketrans("",""), string.punctuation)

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
      itemid = m.group(2)
      itemname = canonicalize_input(m.group(3).replace('-', ' '))

      engine.store_json(itemid, itemname, {
        'name': itemname,
        'id': itemid,
      })
  print 'Done.'

def search(q):
  return engine.search_json(q)

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
