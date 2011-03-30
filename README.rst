######
Exitwp
######

Exitwp is tool primarily aimed for making migration from multiple wordpress blogs to the `jekyll blog engine <https://github.com/mojombo/jekyll/>`_ as easy as possible.

This is a tool that aids batch conversions of wordpress blogs to use with the jekyll blog engine.

By default it will try to convert as much information as possible from wordpress but can also be told to filter the amount of data it converts.

Getting started
===============
 * Check out or download the repository
 * Export one or more wordpress blogs using the wordpress exporter under tools/export in wordpress admin.
 * Put all wordpress xml files in the wp-xml-export directory
 * Run the converter by typing 'python exitwp.py' in the console
 * You should now have all the blogs converted into separate directories under the build directory

Runtime dependencies
====================
 * Python 2.6
 * Pandoc: document conversion from html to markdown and so on... (haskell)
 * PyYAML: Reading configuration files and writing YAML headers (python)
 * Beautiful soup: Parsing and downloading of post images/attachments (python)

Installing python dependencies in ubuntu
----------------------------------------

   sudo apt-get install pandoc

   sudo apt-get install python-yaml python-beautifulsoup

Installing using Using python package installer
-----------------------------------------------

from the checked out root for this project, type:

   pip install -e pip_requirements.txt


 Configuration
=============

Check
