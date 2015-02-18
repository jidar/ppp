import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "ppp",
    version = "0.1",
    author = "Jose Idar",
    author_email = "jose.idar@gmail.com",
    description = ("A PPP report aggregator and report builder"),
    license = "BSD",
    url = "https://github.com/jidar/ppp",
    packages=['ppp'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: BSD License",
    ],
    entry_points = {'console_scripts':['ppp=ppp.cli:entry_point']}
)
