# Copyright 2012 Roland Sieker <ospalh@gmail.com>
# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017 Pu Anlai <https://github.com/InspectorMustache>
# Copyright 2017-2019 Joseph Lorimer <joseph@lorimer.me>
# Inspiration: Tymon Warecki
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

from os.path import basename, exists, join, expanduser
from re import sub
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
import datetime
import hashlib

import requests
from aqt import mw
from gtts import gTTS
import boto3
from urllib.parse import urlparse
import datetime
import hashlib
import hmac

requests.packages.urllib3.disable_warnings()

def download(text, source='google|zh-cn'):
    service, lang = source.split('|')

    path = get_path(text, service, lang)

    if exists(path):
        return basename(path)

    if service == 'google':
        # TODO: should raise ValueError on unsupported lang code
        tts = gTTS(text, lang=lang)
        tts.save(path)
    elif service == 'baidu':
        download_baidu(text, lang, path)
    elif service == 'aws':
        download_aws(text, lang, path)
    else:
        raise NotImplementedError(service)

    return basename(path)


def get_path(text, service, lang):
    filename = '{}_{}_{}.mp3'.format(sanitize(text), service, lang)
    return join(mw.col.media.dir(), filename)


def sanitize(s):
    return sub(r'[\/:\*?"<>\|]', '', s)


def download_baidu(text, lang, path):
    # http://tts.baidu.com/text2audio?lan=zh&ie=UTF-8&text={text}
    def buildUrl(text, lang):
        url_gtts = 'http://tts.baidu.com/text2audio?'
        query = dict(lan=lang, ie='UTF-8', text=text.encode('utf-8'))
        return url_gtts + urlencode(query)

    request = Request(buildUrl(text, lang))
    request.add_header('User-Agent', 'Mozilla/5.0')
    response = urlopen(request, timeout=5)

    if response.code != 200:
        raise ValueError(str(response.code) + ': ' + response.msg)
    with open(path, 'wb') as audio:
        audio.write(response.read())

def download_aws(text, lang, path):
    signer = AWS4Signer(service='polly')
    signer.use_aws_profile('chinese_support_redux')

    url = "https://polly.%s.amazonaws.com/v1/speech" % (signer.region_name)
    post_data = {
        "OutputFormat" : "mp3",
        "Text" : text,
        "VoiceId" : lang,
    }

    res = requests.post(url, json=post_data, auth=signer)

    if res.status_code != 200:
        raise ValueError("Polly Request Failed: Error Code "+str(res.status_code))

    with open(path, 'wb') as audio:
        audio.write(res.content)
