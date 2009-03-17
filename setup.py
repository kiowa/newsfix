#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup

setup(
    name = "GoogleReaderNewspaper",
    version = "0.1",
    description = "Create a newspaper from your google reader tags",
    author = "Alexander Brill",
    author_email = "alex@brill.no",
    url = "http://brill.no",    
    packages = [""],
    py_modules = ["makenewspaper"],
    requires = ["pisa", "html5lib", "pyrfeed"]
)