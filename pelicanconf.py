#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'0x656e'
SITENAME = u'Enes Ergün'
SITESUBTITLE = u"Personel homepage about of my Profession"
SITEURL = 'https://enesergun.net'

PATH = 'content'

TIMEZONE = 'Europe/Istanbul'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Mertcan Gökgöz', 'https://mertcangokgoz.com/'),
         ('Onur Aslan', 'https://onur.im/'),
         ('Ömer İpek', 'http://www.omeripek.com.tr/'),
         ('Canyoupwn.me', 'https://canyoupwn.me/'),
         ('Oğuz Özkeroğlu', 'http://www.oguzozkeroglu.com'),
         ('Ahmet Gürel', 'http://ahmetgurel.com'),
         ('Berk İmran', 'https://berkimran.com.tr'),
         ('Ali Gören', 'https://aligoren.com'),
         ('Emir Kurt', 'https://0xf61.gitlab.io/'),
         ('1v3m', 'https://cybersaxostiger.github.io/'),)

# Social widget
CONTACTS = (('twitter', 'www.twitter.com/0x656e'),
            ('mail', 'info@enesergun.net'))
SOCIAL = (('0x656e', 'www.twitter.com/0x656e'),)
RECENT_POST_COUNT = 10
DISPLAY_RECENT_POSTS_ON_MENU = 5

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
DISQUS_SITENAME = "0x656e"
DISQUS_LOAD_LATER = True
GOOGLE_ANALYTICS = "UA-44262671-1"
THEME = '/home/ka1/Pelican-Cid'
OUTPUT_PATH = '/home/ka1/blogyazilari'
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True
SHARE = True
USE_CUSTOM_MENU = False
PLUGIN_PATHS = ['/home/ka1/Pelican-Cid/plugins']
PLUGINS = ['cid_filters']
