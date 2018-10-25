# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from functools import reduce
from re import findall, sub

from .hanzi import has_hanzi
from .main import config_manager
from .tts import download_sound
from .util import cleanup


def sound(text, source=None):
    from .color import no_color
    from .ruby import hanzi, has_ruby
    from .transcribe import no_accents
    """Returns sound tag for a given Hanzi string.

    If the sound does not already exist in the media directory, then
    attempt to obtain it from the specified source.

    if the specified source is omitted, use the one selected in the
    tools menu.

    If it fails (eg: no network connexion while trying to retrieve
    speech from Google TTS), return empty string.

    Source is either the TTS speech engine name.
    If empty, taking the one from the menu.
    """

    if not has_hanzi(text):
        return ''

    text = cleanup(text)

    if not source:
        source = config_manager.options['speech']

    text = no_color(no_accents(no_sound(text)))
    text = sub(r'<.*?>', '', text)

    if has_ruby(text):
        text = hanzi(text)

    if not text:
        return ''

    options = {
        'Google Mandarin (PRC)': ('google', 'zh-cn'),
        'Google Mandarin (Taiwan)': ('google', 'zh-tw'),
        'Baidu Translate': ('baidu', 'zh'),
    }

    if source in options:
        return '[sound:%s]' % download_sound(text, options[source])

    return ''


def extract_sound_tags(text):
    sound_tags = findall(r'\[sound:.*?\]', text)
    if [] == sound_tags:
        sound_tags=''
    else:
        sound_tags = reduce(lambda a,b:a+b, sound_tags)
    nosound = sub(r'\[sound:.*?\]', r'', text)
    return nosound, sound_tags


def no_sound(text):
    """Remove Anki [sound:xxx.mp3] tag.

    If it isn't removed, it can be duplicated.
    """
    return sub(r'\[sound:.*?]', '', text)
