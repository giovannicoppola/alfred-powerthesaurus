#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2020 hello@clarencecastillo.me
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2017-03-06
# Wednesday, March 23, 2022 updated to Python3 by giovanni
# https://github.com/giovannicoppola/alfred-powerthesaurus
# Sunny ☀️   🌡️+42°F (feels +40°F, 30%) 🌬️←0mph 🌖

"""
Powerthesaurus API
"""


import sys
import json



ICON = 'icon.png'
API_URL = 'https://api.powerthesaurus.org'
WEB_URL = 'https://www.powerthesaurus.org'


def log(s, *args):
    if args:
        s = s % args
    print(s, file=sys.stderr)


def build_thesaurus_item_subtitle(term):
    pos = ' & '.join(term['parts_of_speech'])
    tags = ' '.join('#{}'.format(t) for t in term['tags'])
    return ' | '.join([str(term['rating']), term['word']] + list(filter(lambda s : len(s.strip()), [pos, tags])))
    
def build_thesaurus_item(term, query_type):
    return {
        'title': term['word'],
        'subtitle': build_thesaurus_item_subtitle(term),
        'autocomplete': term['word'],
        'largetext': term['word'],
        'copytext': term['word'],
        'variables': {
            "myURLsyn": term['url_synonyms'],
            "myURLanto": term['url_antonyms']
        },
        'valid': True,
        'quicklookurl': {
            'synonym': term['url_synonyms'],
            'antonym': term['url_antonyms']
        }[query_type],
        'icon': ICON,
        'arg': term['word']
    }

def main():

    from api import PowerThesaurus

    input_text = sys.argv[1] if len(sys.argv) > 1 else ''

    parts = input_text.split(' ', 1)
    query_type = parts[0] if parts else ''
    query = parts[1] if len(parts) > 1 else ''

    if not query:
        return 0


    # initializing the pt (API) object
    pt = PowerThesaurus(API_URL, WEB_URL, logger=log)
    ####################################

#     ###### MAIN CALL TO THE API
#     ##############################
    # a network/HTTP failure or an API change would otherwise dump a traceback
    try:
        term = pt.search_query_match(query)
        # Fetch thesaurus terms from API
        thesaurus_terms = list(pt.thesaurus_query((term or {}).get('id'), query_type))
    except Exception as e:
        log('PowerThesaurus API error: {!r}'.format(e))
        print(json.dumps({"items": [{
            "title": "Could not reach PowerThesaurus",
            "subtitle": "Check your connection and try again",
            "arg": "",
            "icon": {"path": "icons/warning.png"}
        }]}))
        return 0
#     ##############################
    
    
    #log('thesaurus output {!r}'.format(thesaurus_terms))  
    log('thesaurus: found {} {}s for {!r}'.format(len(thesaurus_terms), query_type, query))

    # # Show results
    items = [build_thesaurus_item(t, query_type) for t in (thesaurus_terms or [])]
    
    log (items)
    result = {"items": []}
    
    if not items:
        result= {"items": [{
        "title": 'No {}s found for \"{}\"'.format(query_type, query),
        "subtitle": "Try searching for another word...",
        "arg": "",
        "icon": {

                "path": "icons/warning.png"
            }
        }]}
        print (json.dumps(result))
    else:
        for item in items:
            log(item['quicklookurl'])
            result["items"].append(item)
        
        print (json.dumps(result))

if __name__ == '__main__':
    main()

    