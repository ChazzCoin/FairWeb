from setuptools import setup, find_packages
import os

current = os.getcwd()

setup(
    name='FairWEB',
    version='3.1.2',
    description='Full HTML WebPage Downloader, Parser and Data Extractor. Web Crawler Included.',
    url='https://github.com/chazzcoin/fairweb',
    author='ChazzCoin',
    author_email='chazzcoin@gmail.com',
    license='BSD 2-clause',
    packages=find_packages(),
    package_data={
        'Resources': ['*.txt']
    },
    install_requires=['FCoRE>=1.0.3', 'FairNLP>=1.2.0', 'FairMongo>=1.0.4',
                      'beautifulsoup4==4.9.3', 'newspaper3k==0.2.8'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)