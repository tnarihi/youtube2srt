#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, urllib2
from xml.dom import minidom
from HTMLParser import HTMLParser

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
    return dict(trackDom.attributes.items())


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
    lang = langList[selectedId]
    return lang


def print_lang_list(url):
    videoId = get_video_id(url)
    langList = get_lang_list(videoId)
    print '[Language list]'
    for lang in langList:
        print '%s) %s'%(lang['id'], lang['lang_code'])


def convert_time_format(ftime):
    return '%02d:%02d:%02d,%03d'%(
        int(ftime/3600),
        int(ftime/60)%60,
        (int(ftime)%3600)%60,
        int((ftime - int(ftime)) * 1000)
        )


def print_srt(url, num):
    videoId = get_video_id(url)
    langList = get_lang_list(videoId)
    lang = langList[num]
    captionUrl = CAPTION_URL%(dict(video_id=videoId, **lang))
    capDom = minidom.parse(
        urllib2.urlopen(captionUrl)
        )
    texts = capDom.getElementsByTagName('text')
    hp = HTMLParser()
    for i, text in enumerate(texts):
        fstart = float(text.getAttribute('start'))
        start = convert_time_format(fstart)
        fdur = float(text.getAttribute('dur'))
        dur = convert_time_format(fstart+fdur)
        t = text.childNodes[0].data
        print '%d'%(i)
        print '%s --> %s'%(start, dur)
        print hp.unescape(t).encode(sys.getfilesystemencoding())
        print ''
    

def print_usage_and_exit():
    print >> sys.stderr, """#Print YouYube video caption with SRT format

##USAGE
* Go www.youtube.com and watch a movie.
* Copy the video URL.
* Run this script as below.
    %(prog)s <video url>
* Then you can see the available caption language list.
* Run this script again with the index number of caption language you want to dump.
    %(prog)s <video url> <lang id> > script.srt
"""%{'prog':av[0]}
    sys.exit(1)


if __name__ == '__main__':

    av = sys.argv
    if len(av) == 2:
        print_lang_list(av[1])
    elif len(av) == 3:
        try:
            langId = int(av[2])
        except ValueError:
            print_usage_and_exit()
        print_srt(av[1], langId)
    else:
        print_usage_and_exit()
