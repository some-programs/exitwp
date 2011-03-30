######
Exitwp
######

Exitwp is tool for making migration from one or more wordpress blogs to the `jekyll blog engine <https://github.com/mojombo/jekyll/>`_ as easy as possible.

By default it will try to convert as much information as possible from wordpress but can also be told to filter the amount of data it converts.

The latest version of these docs should always be available at https://github.com/thomasf/exitwp

Known issues
============
 * Image/attachment downloading not implemented
 * This documentation page needs some polish
 * There will probably be issues when migrating non utf-8 encoded wordpress dump files (if they exist)

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

See the `configuration file <https://github.com/thomasf/exitwp/blob/master/config.yaml>`_ for all options.

Some things like handling more post types isnt configuration file configurable atm. you might have to modify the `source code <https://github.com/thomasf/exitwp/blob/master/exitwp.py>`_ to add additional parsing behaviour
