# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
# Inspiration and source of the URL: Tymon Warecki
# Adapted by Thomas TEMPE, thomas.tempe@alysse.org
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html


'''
Download Chinese pronunciations from GoogleTTS
'''

import urllib
import urllib2
import os
import re

from aqt import mw


download_file_extension = u'.mp3'
url_gtts = 'http://translate.google.com/translate_tts?'
user_agent_string = 'Mozilla/5.0'


def get_word_from_google(source, voice = 'zh', append = ''):
    filename, fullpath = get_filename(source + append, download_file_extension)
    if os.path.exists(fullpath):
        return filename
    get_url = build_query_url(source, voice)
    # This may throw an exception
    request = urllib2.Request(get_url)
    request.add_header('User-agent', user_agent_string)
    response = urllib2.urlopen(request, timeout=5)
    if 200 != response.code:
        raise ValueError(str(response.code) + ': ' + response.msg)
    with open(fullpath, 'wb') as audio_file:
        audio_file.write(response.read())
    return filename

def check_resources(source):
    "Only checks for the existence of the file in resources directory, without downloading"
    filename, fullpath = get_filename(source, download_file_extension)
    if os.path.exists(fullpath):
        return True
    return False
    

def build_query_url(source, voice):
    qdict = dict(tl=voice, q=source.encode('utf-8'))
    return url_gtts + urllib.urlencode(qdict)


def get_filename(base, end):
    """Return the media filename for the given title. """
    # Basically stripping the 'invalidFilenameChars'. (Not tested too much).
    base = re.sub('[\\/:\*?"<>\|]', '', base)
    mdir = mw.col.media.dir()
    return base + end, os.path.join(mdir, base + end)
