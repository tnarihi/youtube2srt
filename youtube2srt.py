#! /usr/bin/env python
import sys, re, urllib2
CAPTION_LANG_LIST_URL = "http://video.google.com/timedtext?type=list&v=%s"
CAPTION_URL = "http://video.google.com/timedtext?hl=%(lang_code)s&lang=%(lang_code)s&name=%(name)s&v=%(video_id)s"

def main(url):
    videoId = get_video_id(url)
    # get caption languages list
    langUrl = CAPTION_LANG_LIST_URL%(videoId)
    page = urllib2.urlopen(langUrl)
    for line in page:
        print line

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
