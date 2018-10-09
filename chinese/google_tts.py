# Copyright 2012 Roland Sieker <ospalh@gmail.com>o
# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017 Pu Anlai
# Copyright 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
# Inspiration: Tymon Warecki
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html


from os.path import exists, join
from re import sub

from aqt import mw

from gtts import gTTS


def downloadSound(source, lang='zh-cn'):
    filename, path = getFilename('_'.join([source, 'G', lang]), '.mp3')

    if exists(path):
        return filename

    # should raise ValueError on unsupported lang code
    tts = gTTS(source, lang=lang)
    tts.save(path)

    return filename


def getFilename(base, ext):
    filename = stripInvalidChars(base) + ext
    path = join(mw.col.media.dir(), filename)
    return (filename, path)


def stripInvalidChars(s):
    return sub('[\\/:\*?"<>\|]', '', s)
