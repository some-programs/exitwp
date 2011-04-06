######
Exitwp
######

Exitwp is tool for making migration from one or more wordpress blogs to the `jekyll blog engine <https://github.com/mojombo/jekyll/>`_ as easy as possible.

By default it will try to convert as much information as possible from wordpress but can also be told to filter the amount of data it converts.

The latest version of these docs should always be available at https://github.com/thomasf/exitwp

Getting started
===============
 * `Download <https://github.com/thomasf/exitwp/zipball/master>`_ or clone using ``git clone https://thomasf@github.com/thomasf/exitwp.git``
 * Export one or more wordpress blogs using the wordpress exporter under tools/export in wordpress admin.
 * Put all wordpress xml files in the ``wordpress-xml`` directory
 * Run the converter by typing ``python exitwp.py`` in the console from the directory of the unzipped archive
 * You should now have all the blogs converted into separate directories under the ``build`` directory

Runtime dependencies
====================
 * `Python <http://python.org/>`_ 2.6
 * `Pandoc <http://johnmacfarlane.net/pandoc/>`_ :  document conversion from html to markdown and so on... (haskell)
 * `PyYAML <http://pyyaml.org/wiki/PyYAML>`_ : Reading configuration files and writing YAML headers (python)
 * `Beautiful soup <http://www.crummy.com/software/BeautifulSoup/>`_ : Parsing and downloading of post images/attachments (python)


Installing non python dependencies in ubuntu/debian
---------------------------------------------------

   ``sudo apt-get install pandoc``

Installing python dependencies in ubuntu/debian
-----------------------------------------------

   ``sudo apt-get install python-yaml python-beautifulsoup``

Installing Python dependencies using python package installer (pip)
-------------------------------------------------------------------

From the checked out root for this project, type:

   ``sudo pip install --upgrade  -r pip_requirements.txt``

Note that PyYAML will require other packages to compile correctly under ubuntu/debian, these are installed by typing:

   ``sudo apt-get install libyaml-dev python-dev build-essential``


Configuration/Customization
===========================

See the `configuration file <https://github.com/thomasf/exitwp/blob/master/config.yaml>`_ for all configurable options.

Some things like custom handling of non standard post types is not fully configurable through the config file. You might have to modify the `source code <https://github.com/thomasf/exitwp/blob/master/exitwp.py>`_ to add custom parsing behaviour.

Known issues
============
Near future improvements:
 * Target file names are some times less than optimal.
 * Rewriting of image/attachment links if they are downloaded
 * Meaningful translation/filtering of wikipedia publish statuses into something that usable within a fairly standard jekyll setup.

Things I want to do to learn writing better python code:
 * Refactor code to use less nesting
 * Refactor code to use more try/except tests instead of if statements

Things that might be resolved later on if I find the time:
 * There will probably be issues when migrating non utf-8 encoded wordpress dump files (if they exist).
 * Integrate one or a few basic jekyll site templates to render complete working jekyll blog setups from wordpress exports.
