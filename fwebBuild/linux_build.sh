#!/usr/bin/env bash

# -> Make sure to be in parent directory!
cd ..
# -> Make sure setuptools and wheel are installed/updated
pip3 uninstall FWEB
sudo python3 -m pip install --user --upgrade setuptools wheel
# -> Setup Package
sudo python3 setup.py sdist --format gztar bdist_wheel
# -> Build/Install Package
sudo python3 setup.py build
sudo python3 setup.py install --user
pip3 install .

#sudo python3 setup.py sdist
#sudo python3 setup.py build