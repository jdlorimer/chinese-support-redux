# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
# Inspiration and source of the URL: Tymon Warecki
# Adapted by Thomas TEMPE, thomas.tempe@alysse.org
#
# License: AGNU GPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html


'''
Download pronunciations from GoogleTTS
'''

import tempfile
import urllib
import urllib2
import os
import os.path

from process_audio import process_audio, unmunge_to_mediafile, get_filename

download_file_extension = u'.mp3'

url_gtts = 'http://translate.google.com/translate_tts?'

user_agent_string = 'Mozilla/5.0'


def get_word_from_google(source, language="zh"):
    filename, fullpath =get_filename(source, download_file_extension)
    if os.path.exists(fullpath):
	    return filename
    get_url = build_query_url(source, language)
    print "url", get_url
    # This may throw an exception
    request = urllib2.Request(get_url)
    request.add_header('User-agent', user_agent_string)
    response = urllib2.urlopen(request)
    if 200 != response.code:
        raise ValueError(str(response.code) + ': ' + response.msg)
    temp_file = tempfile.NamedTemporaryFile(delete=False,
                                            suffix=download_file_extension)
    temp_file.write(response.read())
    temp_file.close()
    extras = dict(source='GoogleTTS')
    try:
        return process_audio(temp_file.name, source, download_file_extension)
    except:
        return unmunge_to_mediafile(temp_file.name, source,
                                    download_file_extension)


def build_query_url(source, language):
        qdict = {}
        qdict['tl'] = language.encode('utf-8')
        qdict['q'] = source.encode('utf-8')
        return url_gtts + urllib.urlencode(qdict)
