#!/bin/bash -e

pushd data > /dev/null
touch foo
rm *

for i in {0..7}; do
  curl -o item$i http://www.wowhead.com/sitemap=item/$i
done

for i in {0..8}; do
  curl -o spell$i http://www.wowhead.com/sitemap=spell/$i
done

curl -o itemset1 http://www.wowhead.com/sitemap=itemset/1
curl -o transmogset1 http://www.wowhead.com/sitemap=transmog-set/1

# Least priority first - order matters
# We want items to override their associated spells whenever possible
cat spell* item* itemset* transmogset* > all
popd
