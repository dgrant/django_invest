#!/bin/sh
rm -rf env.bak
mv env env.bak
sudo apt-get update
sudo apt-get install python-setuptools libmysqlclient-dev python-dev
sudo easy_install pip
sudo pip install --upgrade virtualenv
virtualenv --distribute env
env/bin/pip install --download-cache=~/.pip-cache -r requirements.txt
