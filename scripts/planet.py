#!/usr/bin/env python3

import csv
import html
import json
import feedparser

import datetime
import socket
import time

# Configuration

ARTICLES_PATH       = 'static/json/articles.json'
PLANET_TITLE        = 'CSE-40842-FA25 Planet'
PLANET_DESCRIPTION  = 'All blog entries for CSE 40842 Hackers in the Bazaar (Fall 2025)'
PLANET_URL          = 'https://pnutz.h4x0r.space/courses/cse.40842.fa25/'

# Load existing articles

try:
    articles_json = json.load(open(ARTICLES_PATH))
except IOError:
    articles_json = {}

socket.setdefaulttimeout(5)

# Add every entry from every blog feed

for blog in csv.DictReader(open('data/blogs.csv')):
    feed_data = feedparser.parse(blog['Feed'])

    for entry in feed_data.entries:
        timestamp = entry.get('updated_parsed', entry.get('published_parsed', None))
        timestamp = time.mktime(timestamp) if timestamp else time.time()
        try:
            entry_title = html.escape(entry['title'])
            entry_id    = entry['link'] + entry_title
            entry_id    = entry.get('id', entry_id) or entry_id
        except KeyError:
            continue

        articles_json[entry_id] = {
            'author'    : '@' + blog['NetID'],
            'timestamp' : timestamp,
            'published' : entry.get('updated', entry.get('published')),
            'title'     : entry_title,
            'link'      : entry['link'],
            'source'    : blog['Feed'],
        }

# Store articles

with open(ARTICLES_PATH, 'w') as articles_file:
    json.dump(articles_json, articles_file)

# Generate planet

print('''<rss version="2.0">
<channel>
<title>{planet_title}</title>
<link>{planet_url}</link>
<description>
{planet_description}
</description>'''.format(planet_title       = PLANET_TITLE,
                         planet_url         = PLANET_URL,
                         planet_description = PLANET_DESCRIPTION))

for article_id, article in sorted(articles_json.items(), key=lambda a: a[1]['timestamp'], reverse=True):
    print('''<item>
<title>{article_title}</title>
<author>{article_author}</author>
<link>{article_link}</link>
<source>{article_source}</source>
<guid>{article_id}</guid>
<pubDate>{article_published}</pubDate>
</item>'''.format(article_title     = article['title'],
                  article_author    = article['author'],
                  article_link      = article['link'],
                  article_source    = article['source'],
                  article_id        = article_id,
                  article_published = article['published']))

print('''</channel>
</rss>''')
