#!/usr/bin/env bash
set -e
echo "**** Box setup ***"

echo "* mkdir /kitchen"
mkdir -p /kitchen

#echo "* cp -ar /mnt/shared /kitchen"
#cp -r /mnt/shared/. /kitchen
echo "* ln -sf /mnt/shared /kitchen"
ln -sf /mnt/shared/* /kitchen/

echo "* cd /kitchen"
cd /kitchen/*

echo "* python tests/travis_run.py"
python tests/travis_run.py

