from setuptools import setup, find_packages
import os

current = os.getcwd()

setup(
    name='FairWeb',
    version='1.0.0',
    description='A complete Python Package for Downloading Articles and WebPages.',
    url='https://github.com/chazzcoin/FWEB',
    author='ChazzCoin',
    author_email='chazzcoin@gmail.com',
    license='BSD 2-clause',
    packages=find_packages(),
    install_requires=['requests==2.27.1', 'newspaper3k~=0.2.8', 'python-dateutil~=2.7.5', 'beautifulsoup4==4.9.3'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)