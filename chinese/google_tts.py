# -*- coding: utf-8 -*-
# Copyright 2012 Roland Sieker <ospalh@gmail.com>o
# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017 Pu Anlai
# Copyright 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
# Inspiration: Tymon Warecki
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html


from os.path import exists
import os
import re

from aqt import mw

from .lib.gtts import gTTS


def get_word_from_google(source, lang='zh'):
    filename, path = getFilename('_'.join([source, 'G', lang]), '.mp3')

    if exists(path):
        return filename

    tts = gTTS(source, lang=lang)
    tts.save(path)

    return filename


def getFilename(base, ext):
    filename = stripInvalidChars(base) + ext
    path = os.path.join(mw.col.media.dir(), filename)
    return (filename, path)


def stripInvalidChars(s):
    return re.sub('[\\/:\*?"<>\|]', '', s)
