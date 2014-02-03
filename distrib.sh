#!/bin/sh
mkdir distrib
rm -rf distrib/*
cp -ar Chinese_support.py chinese distrib
cd distrib
find -name \*~ |xargs rm
find -name \*.pyc |xargs rm
cd chinese
rm chinese_addon_config.json
rm edit_behavior.py
touch edit_behavior.py
cd db
./update --cleanup
rm -rf tmp
cd ../..
zip -r chinese_support Chinese_support.py chinese --exclude \*~ \#* \*.orig Logo .DS_Store
