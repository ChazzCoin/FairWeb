#!/usr/bin/env bash

# -> Make sure to be in parent directory!
cd ..
# -> Make sure setuptools and wheel are installed/updated
sudo python3 -m pip install --user --upgrade setuptools wheel
# -> Setup Package
sudo python3 setup.py sdist --format gztar bdist_wheel
# -> Build/Install Package
sudo python3 setup.py build --user
sudo python3 setup.py install --user