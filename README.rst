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
 * `Download <https://github.com/thomasf/exitwp/zipball/master>`_ or clone using ``git clone https://thomasf@github.com/thomasf/exitwp.git``
 * Export one or more wordpress blogs using the wordpress exporter under tools/export in wordpress admin.
 * Put all wordpress xml files in the ``wordpress-xml`` directory
 * Run the converter by typing ``python exitwp.py`` in the console from the directory of the unzipped archive
 * You should now have all the blogs converted into separate directories under the ``build`` directory

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

   (NOTE: pip_requirements.txt not written yet)


 Configuration/Customization
============================

See the `configuration file <https://github.com/thomasf/exitwp/blob/master/config.yaml>`_ for all configurable options.

Some things like custom handling of non standard post types is not fully configurable through the config file. You might have to modify the `source code <https://github.com/thomasf/exitwp/blob/master/exitwp.py>`_ to add custom parsing behaviour.
