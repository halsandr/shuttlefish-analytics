#!/usr/bin/env bash

rm -r dist/
pyinstaller -F Shuttlefish_Analytics.py
rm -r build/
rm Shuttlefish_Analytics.spec
cp client_secrets.json dist/client_secrets.json