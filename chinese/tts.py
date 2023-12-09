# Copyright © 2012 Roland Sieker <ospalh@gmail.com>
# Copyright © 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017 Pu Anlai <https://github.com/InspectorMustache>
# Copyright © 2019 Oliver Rice <orice@apple.com>
# Copyright © 2017-2021 Joseph Lorimer <joseph@lorimer.me>
# Inspiration: Tymon Warecki
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

from .aws import AWS4Signer

from os.path import basename, exists, join
from re import sub
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import requests
from aqt import mw
from gtts import gTTS
from gtts.tts import gTTSError

requests.packages.urllib3.disable_warnings()


class AudioDownloader:
    def __init__(self, text, source='google|zh-CN'):
        self.text = text
        self.service, self.lang = source.split('|')
        self.path = self.get_path()
        self.func = {
            'google': self.get_google,
            'baidu': self.get_baidu,
            'aws': self.get_aws,
        }.get(self.service)

    def get_path(self):
        filename = '{}_{}_{}.mp3'.format(
            self.sanitize(self.text), self.service, self.lang
        )
        return join(mw.col.media.dir(), filename)

    def sanitize(self, s):
        return sub(r'[/:*?"<>|]', '', s)

    def download(self):
        if exists(self.path):
            return basename(self.path)

        if not self.func:
            raise NotImplementedError(self.service)

        self.func()

        return basename(self.path)

    def get_google(self):
        tts = gTTS(self.text, lang=self.lang, tld='com')
        try:
            tts.save(self.path)
        except gTTSError as e:
            print('gTTS Error: {}'.format(e))

    def get_baidu(self):
        query = {
            'lan': self.lang,
            'ie': 'UTF-8',
            'text': self.text.encode('utf-8'),
        }

        url = 'http://tts.baidu.com/text2audio?' + urlencode(query)
        request = Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0')
        response = urlopen(request, timeout=5)

        if response.code != 200:
            raise ValueError('{}: {}'.format(response.code, response.msg))

        with open(self.path, 'wb') as audio:
            audio.write(response.read())

    def get_aws(self):
        signer = AWS4Signer(service='polly')
        signer.use_aws_profile('chinese_support_redux')

        url = 'https://polly.%s.amazonaws.com/v1/speech' % (signer.region_name)
        query = {
            'OutputFormat': 'mp3',
            'Text': self.text,
            'VoiceId': self.lang,
        }

        response = requests.post(url, json=query, auth=signer)

        if response.status_code != 200:
            raise ValueError(
                'Polly Request Failed: Error Code {}'.format(
                    response.status_code
                )
            )

        with open(self.path, 'wb') as audio:
            audio.write(response.content)
