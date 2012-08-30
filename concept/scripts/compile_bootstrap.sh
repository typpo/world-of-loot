#!/bin/bash -e

rm css/bootstrap.css
lessc bootstrap/less/bootstrap.less > css/bootstrap.css
echo "Done."
