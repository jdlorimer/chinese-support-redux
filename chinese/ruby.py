# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from re import search, sub

from .bopomofo import bopomofo
from .color import no_color
from .main import dictionary
from .sound import no_sound, sound


def ruby(words, transcription=None, only_one=False, try_dict_first=True):
    '''Convert hanzi to ruby notation.

    For use with {{Ruby:fieldname}} on the card template.

    If not specified, use the transcription type set in the menubar.

    if try_dict_first, looks up sequences of characters in the
    selected words dictionary to supply a better transcription.

    If not specified, insert all possible pinyin words for characters not found
    in words dictionary.
    '''
    if not transcription:
        transcription = config_manager.options['transcription']

    rubified = []
    for text in words:
        text = sub(r'[［【]', '[', text)
        text = sub(r'[］】]', ']', text)
        text = no_color(text)
        text = no_sound(text)
        # make sure sound tag isn't confused with hanzi
        text = sub(r'([\u3400-\u9fff])(\[sound:)', r'\1 \2', text)

        def insert_multiple_pinyin_sub(p):
            hanzi = p.group(1)
            t = dictionary.get_pinyin(hanzi)
            if not t:
                return p.group()
            t = t.split(' ')
            s = ''
            hanzi = p.group(1)
            while hanzi:
                if transcription == 'Pinyin':
                    s += hanzi[0] + '[' + t.pop(0) + ']'
                elif transcription == 'Bopomofo':
                    s += hanzi[0] + '['
                    s += bopomofo(no_accents(t.pop(0))) + ']'
                hanzi = hanzi[1:]
            return s + p.group(2)

        def insert_pinyin_sub(p):
            t = get_char_transcription(p.group(1), transcription, only_one)
            return p.group(1) + '[' + t + ']' + p.group(2)

        text += '%'
        if try_dict_first and transcription in ['Pinyin', 'Bopomofo']:
            text = sub(
                r'([\u3400-\u9fff]+)([^[])',
                insert_multiple_pinyin_sub,
                text
            )
        text = sub(r'([\u3400-\u9fff])([^[])', insert_pinyin_sub, text)
        text = sub(r'([\u3400-\u9fff])([^[])', insert_pinyin_sub, text)
        text = text[:-1]
        rubified.append(text + sound(text))

    return rubified


def has_ruby(text):
    return search(r'[\u3400-\u9fff]\[.+\]', text)


def hide_ruby(text):
    from .transcribe import no_tone
    """Append hidden hanzi and toneless pinyin to a ruby string,
    to make a note searchable in the 'browse' window.
    """
    t = no_tone(ruby_top(text))
    t += no_color(ruby_bottom(text)).replace(' ', '')
    return hide(text, t)


def ruby_top(text):
    return sub(r' ?([^ >]+?)\[(.+?)\]', r'\2 ', no_sound(text))


def ruby_bottom(text):
    return sub(r' ?([^ >]+?)\[(.+?)\]', r'\1 ', no_sound(text))


def hanzi(text):
    """Returns just the hanzi from a Ruby notation.

    Example: '你[nǐ][You]' becomes '你'.
    """
    text = sub(r'([\u3400-\u9fff])(\[[^[]+?\])', r'\1', text)
    text = sub(r'\[sound:.[^[]+?\]', '', text)
    text = sub(r'([^\u3400-\u9fff])\[[^[]+?\]\s*$', r'\1', text)
    return text
