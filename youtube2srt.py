#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, urllib2
from xml.dom import minidom

CAPTION_LANG_LIST_URL = "http://video.google.com/timedtext?type=list&v=%s"
CAPTION_URL = "http://video.google.com/timedtext?hl=%(lang_code)s&lang=%(lang_code)s&name=%(name)s&v=%(video_id)s"

def main(url):
    videoId = get_video_id(url)
    # get caption languages list
    langUrl = CAPTION_LANG_LIST_URL%(videoId)
    page = urllib2.urlopen(langUrl)
    langDom = minidom.parse(page)
#    print langDom.toxml()
    tracks = langDom.getElementsByTagName('track')
    while True:
        print 'Here are the available caption langages'
        for track in tracks:
            langId =  int(track.getAttribute('id'))
            langCode = track.getAttribute('lang_code')
            langDefault = track.getAttribute('lang_default')
            langOrig = track.getAttribute('lang_original')
            langTrasl = track.getAttribute('lang_translated')
            name = track.getAttribute('name')
            print ' %d) lang_code=%s'%(langId, langCode)
        try:
            selectedId = int(raw_input('Select number:'))
        except ValueError:
            print >> sys.stderr, 'Input number.'
            continue
        if (selectedId > len(tracks)) or (selectedId < 0):
            print >> sys.stderr, '!Input correct number'
            continue
        break
    track = tracks[selectedId]
    langCode = track.getAttribute('lang_code')
    print langCode



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
    
if __name__ == '__main__':

    av = sys.argv
    if len(av) != 2:
        print >> sys.stderr, 'usage: %s <Youtube video URL>'%av[0]
        sys.exit(1)
    main(av[1])
