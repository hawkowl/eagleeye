#!/usr/bin/env python

from distutils.core import setup

setup(
	name = "eagleeye",
	version = "0.1.0",
	author = "HawkOwl",
	author_email = "hawkowl@outlook.com",
	description = "EagleEye is a library for metrics reporting, using Twisted.",
	long_description = "EagleEye is a library for metrics reporting, using Twisted.",
	keywords = ["twisted", "riemann", "metrics"],
	url = "https://github.com/hawkowl/eagleeye",
	packages = ['eagleeye', 'eagleeye.riemann'],
	classifiers = [
		"Development Status :: 3 - Alpha",
		"License :: OSI Approved :: MIT License",
		"Framework :: Twisted",
		"Topic :: System :: Monitoring"
	],
)