#!/bin/sh
rm -rf env.bak
mv env env.bak
virtualenv --distribute --no-site-packages env
env/bin/pip install -r requirements.txt
