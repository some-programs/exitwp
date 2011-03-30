#!/usr/bin/env python

from xml.etree.ElementTree import ElementTree
from subprocess import call, PIPE, Popen
import os, codecs
from datetime import datetime
from glob import glob
import re
import sys
import yaml
import tempfile
from BeautifulSoup import BeautifulSoup as bs


'''
Import

Tested with Wordpress 3.1 and jekyll trunk 2011-03-26
pandoc is required to be installed if conversion from
html will be done.
'''
######################################################
# Configration
######################################################
config=yaml.load(file('config.yaml','r'))
wp_exports=config['wp_exports']
build_dir=config['build_dir']
download_images = config['download_images']
target_format=config['target_format']
taxonomy_filter = set(config['taxonomies']['filter'])
taxonomy_entry_filter = config['taxonomies']['entry_filter']
taxonomy_name_mapping = config['taxonomies']['name_mapping']
item_type_filter = set(config['item_type_filter'])
date_fmt=config['date_format']

def html2fmt(html, target_format):
    target_format='markdown'
    if (target_format=='html'):
        return html
    else:
        # This is like very stupid but I was having troubles with unicode encodings and process.POpen
        f=codecs.open('pandoc.in', 'w', encoding='utf-8')
        f.write(html)
        f.close()
        call(["pandoc","-f","html","-o", "pandoc.out", "-t",target_format, "pandoc.in"])
        f=codecs.open('pandoc.out', 'r', encoding='utf-8')
        lines=[]
        for line in f: lines.append(line)
        f.close()
        os.remove('pandoc.in')
        os.remove('pandoc.out')
        return ''.join(lines)

def parse_wp_xml(file):
    ns = {
        '':'', #this is the default namespace
        'excerpt':"{http://wordpress.org/export/1.1/excerpt/}",
        'content':"{http://purl.org/rss/1.0/modules/content/}",
        'wfw':"{http://wellformedweb.org/CommentAPI/}",
        'dc':"{http://purl.org/dc/elements/1.1/}",
        'wp':"{http://wordpress.org/export/1.1/}"
    }

    tree=ElementTree()

    print "reading: " + wpe

    root=tree.parse(file)
    c=root.find('channel')

    def parse_header():
        return {
            "title": unicode(c.find('title').text),
            "link": unicode(c.find('link').text),
            "description" : unicode(c.find('description').text)
        }

    def parse_items():
        export_items=[]
        xml_items=c.findall('item')
        for i in xml_items:
            taxanomies=i.findall('category')
            export_taxanomies={}
            for tax in taxanomies:
                t_domain=unicode(tax.attrib['domain'])
                t_entry=unicode(tax.text)
                if not (t_domain in taxonomy_filter) and not (taxonomy_entry_filter.has_key(t_domain) and taxonomy_entry_filter[t_domain]==t_entry):
                    if not export_taxanomies.has_key(t_domain):
                            export_taxanomies[t_domain]=[]
                    export_taxanomies[t_domain].append(t_entry)

            def gi(q, unicode_wrap=True):
                namespace=''
                tag=''
                if q.find(':') > 0: namespace, tag=q.split(':',1)
                else: tag=q
                result=i.find(ns[namespace]+tag).text
                if unicode_wrap: result=unicode(result)
                return result

            export_item = {
                 'title' : gi('title'),
                 'author' : gi('dc:creator'),
                 'date' : gi('wp:post_date'),
                 'slug' : gi('wp:post_name'),
                 'status' : gi('wp:status'),
                 'type' : gi('wp:post_type'),
                 'wp_id' : gi('wp:post_id'),
                 'taxanomies' : export_taxanomies,
                 'body' : gi('content:encoded'),
               }
            export_items.append(export_item)

        return export_items

    return {
        'header': parse_header(),
        'items': parse_items(),
    }


def write_jekyll(data, target_format):

    sys.stdout.write("writing")

    def get_blog_path(data, path_infix='jekyll'):
        name=data['header']['link']
        name=re.sub('^https?','',name)
        name=re.sub('[^A-Za-z0-9_.-]','',name)
        return os.path.normpath(build_dir + '/' + path_infix + '/' +name)

    blog_dir=get_blog_path(data)

    def get_full_dir(dir):
        full_dir=os.path.normpath(blog_dir+'/'+dir)
        if (not os.path.exists(full_dir)):
            os.makedirs(full_dir)
        return full_dir

    def open_file(file):
        f=codecs.open(file, 'w', encoding='utf-8')
        return f


    def get_filename(item, date_prefix=False, dir=''):
        full_dir=get_full_dir(dir)
        filename_parts=[full_dir,'/']
        if (date_prefix):
            dt=datetime.strptime(item['date'],date_fmt)
            filename_parts.append(dt.strftime('%Y-%m-%d'))
            filename_parts.append('-')

        s_title=item['slug']
        if not s_title or s_title == '': s_title=item['title']
        if s_title == '': s_title='untitled'
        s_title=s_title.replace(' ','_')
        s_title=re.sub('[^a-zA-Z0-9_-]','', s_title)
        filename_parts.append(s_title)
        filename_parts.append('.')
        filename_parts.append(target_format)
        return ''.join(filename_parts)

    for i in data['items']:
        sys.stdout.write(".")
        sys.stdout.flush()
        out=None
        yaml_header = {
          'title' : i['title'],
          'date' : i['date'],
          'author' : i['author'],
          'slug' : i['slug'],
          'status' : i['status'],
          'wordpress_id' : i['wp_id'],
        }

        if i['type'] == 'post':
            out=open_file(get_filename(i, date_prefix=True, dir='_posts'))
            yaml_header['layout']='post'
        elif i['type'] == 'page':
            out=open_file(get_filename(i))
            yaml_header['layout']='page'
        elif i['type'] in item_type_filter:
            pass
        else:
            print "Unknown item type :: " +  i['type']

        if out is not None:
            def toyaml(data):
                return yaml.safe_dump(data, allow_unicode=True, default_flow_style=False).decode('utf-8')

            tax_out={}
            for taxonomy in i['taxanomies']:
                for tvalue in i['taxanomies'][taxonomy]:
                    t_name=taxonomy_name_mapping.get(taxonomy,taxonomy)
                    if t_name not in tax_out: tax_out[t_name]=[]
                    tax_out[t_name].append(tvalue)

            out.write('---\n')
            if len(yaml_header)>0: out.write(toyaml(yaml_header))
            if len(tax_out)>0: out.write(toyaml(tax_out))

            out.write('---\n\n')
            out.write(html2fmt(i['body'], target_format))
            out.close()
    print "\n"


wp_exports=glob(wp_exports+'/*.xml')
for wpe in wp_exports:
    data=parse_wp_xml(wpe)
    write_jekyll(data, target_format)

print 'done'
