#!/usr/bin/env python
"""
Usage:
    findme.py <query>
    findme.py -h | --help | --version

"""
from __future__ import absolute_import, print_function
from __init__ import __version__
from docopt import docopt
from pyquery import PyQuery as pg
import re
import yaml
import json
import requests
from urllib import quote as url_quote
from urllib import unquote as url_unquote

SEARCH_QUERY = 'http://www.google.com/search?q={0}'
SOURCES = ['linkedin']
RE_LINK = re.compile('.*q=(.*?)&.*')
RE_GITHUB = re.compile('.*com/([^\/]*)\?.*')
GITHUB_URL = 'https://api.github.com/users/{0}/repos'

with open('profiles.yaml', 'r') as profiles_file:
    profile_configs = yaml.load(profiles_file)

#print(profile_configs)

def get_profile(link):
    profile = None
    link_source = None
    if 'linkedin' in link:
        link_source = 'linkedin'
        profile_config = profile_configs[link_source]
        for config in profile_config:
            if re.match(config['pattern'], link):
                break

        is_list = config['is_list']
        copy_config = dict([(k,v) for k,v in config.iteritems()
           if k not in ['pattern', 'is_list']])

        if not is_list:
            profile = get_profile_by_page(link, copy_config)
        if profile:
            profile['%s_url' % link_source] = link
    elif 'github' in link:
        match_result = RE_GITHUB.match(link)
        if match_result:
            username = match_result.groups()[0]
            content = requests.get(GITHUB_URL.format(username)).text
            data = json.loads(content)
            langs = []
            for r in data:
                lang = r['language']
                if lang and lang not in langs:
                    langs.append(lang)
            profile = {}
            profile['skills'] = ','.join(langs)
    return profile


def get_profile_by_page(link, config):
    html = pg(requests.get(link).text)
    profile = {}

    for k, v in config.iteritems():
        if isinstance(v, list):
            for i in v:
                result = html(i)
                if result:
                    break
        else:
            result = html(v)

        if len(result) > 0:
            result_set = []
            for r in result:
                if r.tag == 'img':
                    result_text = r.attrib['src']
                else:
                    result_text = r.text_content()
                result_text = result_text.strip()
                if result_text not in result_set:
                    result_set.append(result_text)
            profile[k] = ','.join(result_set)
        else:
            profile[k] = result.text().strip()

    return profile


def get_profiles(name):

    links = get_links(name)
    #print('Links: ', links)

    if not links:
        return

    profiles = []
    for link in links:
        profile = get_profile(link)
        if profile:
            profiles.append(profile)

    return profiles


def get_links(text):
    query = SEARCH_QUERY.format(url_quote(text))
    #print('Query: ', query)

    html = pg(requests.get(query).text)
    links = [a.attrib['href'] for a in html('.r')('a')]
    result = []

    for link in links:
        # q={url}
        match_result = RE_LINK.match(link)
        if not match_result:
            continue
        link = match_result.groups()[0]
        result.append(url_unquote(link))

    return result


def merge_profiles(profiles):
    # merge profiles
    profile = {}
    for p in profiles:
        if not profile:
            profile.update(p)
        else:
            for k, v in p.iteritems():
                if k in profile:
                    current_value = profile[k]
                    if isinstance(current_value, (str, unicode)):
                        profile[k] = ','.join([current_value, v])
                    elif isinstance(current_value, list):
                        profile[k] = current_value.extend(v)
    return profile


def command_line_options():
    args = docopt(__doc__, version=__version__)

    if not args['<query>']:
        return

    profiles = get_profiles(args['<query>'])

    profile = merge_profiles(profiles)

    print(json.dumps(profile))
    name = str(args['<query>'])
    f1 = open(name.replace(" ", "_").replace('\n','') + '.json', 'w')
    f1.write(json.dumps(profile) + '\n')
    f1.close()

if __name__ == '__main__':
    command_line_options()
