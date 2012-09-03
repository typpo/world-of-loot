#!/bin/bash -e

pushd data > /dev/null
touch foo
rm *

for i in {1..7}; do
  wget http://www.wowhead.com/sitemap=item/$i
done

for i in {1..8}; do
  wget http://www.wowhead.com/sitemap=spell/$i
done

wget http://www.wowhead.com/sitemap=itemset/1
wget http://www.wowhead.com/sitemap=transmog-set/1

cat * > all
popd
