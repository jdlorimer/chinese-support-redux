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
url_gtts = 'http://tts.baidu.com/text2audio?'
user_agent_string = 'Mozilla/5.0'

# http://tts.baidu.com/text2audio?lan=zh&ie=UTF-8&text=%E4%BD%A0%E5%9C%A8%E5%B9%B2%E4%BB%80%E4%B9%88



def get_word_from_baidu(source, lang="zh"):
    filename, fullpath = get_filename("_".join([source, "B", lang]), download_file_extension)
    if os.path.exists(fullpath):
        return filename
    get_url = build_query_url(source, lang)
    # This may throw an exception
    request = urllib2.Request(get_url)
    request.add_header('User-agent', user_agent_string)
    response = urllib2.urlopen(request, timeout=5)
    if 200 != response.code:
        raise ValueError(str(response.code) + ': ' + response.msg)
    with open(fullpath, 'wb') as audio_file:
        audio_file.write(response.read())
    return filename


def build_query_url(source, lang):
    qdict = dict(lan=lang, ie="UTF-8", text=source.encode('utf-8'))
    return url_gtts + urllib.urlencode(qdict)


def get_filename(base, end):
    """Return the media filename for the given title. """
    # Basically stripping the 'invalidFilenameChars'. (Not tested too much).
    base = re.sub('[\\/:\*?"<>\|]', '', base)
    mdir = mw.col.media.dir()
    return base + end, os.path.join(mdir, base + end)
