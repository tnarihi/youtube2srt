#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, urllib2
from xml.dom import minidom

CAPTION_LANG_LIST_URL = "http://video.google.com/timedtext?type=list&v=%s"
CAPTION_URL = "http://video.google.com/timedtext?hl=%(lang_code)s&lang=%(lang_code)s&name=%(name)s&v=%(video_id)s"

def get_video_id(url):
    """
    Get 'v' option value
    """
    m = re.search(r".*/*(\?|&)v=([\w-]*)", url)
    if m:
        return m.group(2)
    else:
        print >> sys.stderr, 'cannot parse youtube video id.'
        sys.exit(1)
    
def get_lang_attrs(trackDom):
    keys = trackDom.attributes.keys()
    r = {}
    for key in keys:
        r[key] = trackDom.getAttribute(key)
    return r

def get_lang_list(videoId):
    langUrl = CAPTION_LANG_LIST_URL%(videoId)
    page = urllib2.urlopen(langUrl)
    langDom = minidom.parse(page)
    tracks = langDom.getElementsByTagName('track')
    langList = [get_lang_attrs(track) for track in tracks]
    return langList

def select_lang(langList):
    while True:
        print '\nHere are the available caption langages:'
        for lang in langList:
            print ' %s) %s'%(lang['id'], lang['lang_code'])
        try:
            selectedId = int(raw_input('Select number:'))
        except ValueError:
            print >> sys.stderr, 'Error: Input number'
            continue
        if (selectedId > len(langList)-1) or (selectedId < 0):
            print >> sys.stderr, 'Error: Input correct number'
            continue
        break
    langCode = langList[selectedId]['lang_code']
    return langCode

def main(url):
    videoId = get_video_id(url)
    langList = get_lang_list(videoId)
    langCode = select_lang(langList)
    print langCode

if __name__ == '__main__':

    av = sys.argv
    if len(av) != 2:
        print >> sys.stderr, 'usage: %s <Youtube video URL>'%av[0]
        sys.exit(1)
    main(av[1])
