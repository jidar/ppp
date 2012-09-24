import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "ppp",
    version = "1.0",
    author = "Jose Idar",
    author_email = "joseidar@gmail.com",
    description = ("A PPP report aggregator and report builder"),
    license = "BSD",
    url = "https://github.com/jidar/ppp",
    packages=['pppengine','scripts'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: BSD License",
    ],
    entry_points = {'console_scripts':['ppp=scripts.ppp:main']}
)