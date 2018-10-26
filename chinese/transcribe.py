# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from re import compile, IGNORECASE, match, search, sub

from .bopomofo import bopomofo
from .consts import (
    accents,
    base_letters,
    jyutping_finals,
    jyutping_inits,
    jyutping_standalones,
    pinyin_finals,
    pinyin_inits,
    pinyin_standalones,
    vowel_decorations,
    vowel_tone_dict,
)
from .hanzi import has_hanzi
from .main import config_manager, dictionary
from .ruby import has_ruby
from .util import cleanup


def pinyin_re_sub():
    return '(({})({})[1-5]?|({})[1-5]?)'.format(
        pinyin_inits, pinyin_finals, pinyin_standalones)

pinyin_re = pinyin_re_sub()
pinyin_two_re = compile("(?P<one>"+pinyin_re+")(?P<two>"+pinyin_re+")", IGNORECASE)


def jyutping_re_sub():
    return '(({})({})[1-6]?|({})[1-6]?)'.format(
        jyutping_inits, jyutping_finals, jyutping_standalones)

jyutping_re = jyutping_re_sub()
jyutping_two_re = compile("(?P<one>"+jyutping_re+")(?P<two>"+jyutping_re+")", IGNORECASE)


def transcribe(words, transcription=None, only_one=True):
    """Converts to specified transcription.

    Example: 你 becomes nǐ (transcription="Pinyin", only_one=True)

    Pinyin, Taiwan Pinyin and Bopomofo: lookup in local words dictionaries
    first, and use characters dictionary as a backup.

    If no transcription is specified, use the transcription set in the menu.
    """

    words = list(filter(has_hanzi, words))
    transcribed = []

    if not words:
        return transcribed

    for text in words:
        text = cleanup(text)
        if not text:
            transcribed.append('')
        if not transcription:
            transcription = config_manager.options['transcription']
        if transcription == 'Pinyin':
            transcribed.append(dictionary.get_pinyin(text, taiwan=False))
        elif transcription == 'Pinyin (Taiwan)':
            transcribed.append(dictionary.get_pinyin(text, taiwan=True))
        elif transcription == 'Cantonese':
            transcribed.append(dictionary.get_cantonese(text, only_one))
        elif transcription == 'Bopomofo':
            r = dictionary.get_pinyin(text, taiwan=True)
            transcribed.append(bopomofo(no_accents(r)))
        else:
            transcribed.append('')

    return transcribed


def get_char_transcription(hanzi, transcription=None):
    if not transcription:
        transcription = config_manager.options['transcription']
    if transcription == 'Pinyin':
        return dictionary.get_pinyin(hanzi)
    if transcription == 'Pinyin (Taiwan)':
        return dictionary.get_pinyin(hanzi, taiwan=True)
    if transcription == 'Cantonese':
        return dictionary.get_cantonese(hanzi)
    if transcription == 'Bopomofo':
        return bopomofo(dictionary.get_pinyin(hanzi, taiwan=True))
    return str()


def add_diaeresis(text):
    return sub('v', 'ü', text)


def accentuate(syllables):
    """Add accents to pinyin.

    Examples:
        - ni2 becomes ní
        - ní4 becomes nì (to make correction easier)

    Note: also removes coloring.
    """

    from .color import no_color

    if (config_manager.options['transcription']
            not in ['Pinyin', 'Pinyin (Taiwan)']):
        return syllables

    def _accentuate(p):
        pinyin = p.group(1)
        tone = p.group(2)
        if pinyin == 'tone':
            return pinyin + tone
        pinyin = no_tone(pinyin)
        for v in 'aeouüviAEOUÜVI':
            if pinyin.find(v) > -1:
                try:
                    return sub(
                        v,
                        vowel_decorations[int(tone)][v.lower()],
                        pinyin,
                        count=1
                    )
                except (KeyError, IndexError):
                    pass
        return pinyin

    accentuated = []
    for text in syllables:
        text = no_color(text)
        text = sub(
            r'([a-z]*[aeiouüÜv' + accents + r'][a-zü]*)([1-5])',
            _accentuate,
            text,
            flags=IGNORECASE
        )
        accentuated.append(text)

    return accentuated


def no_accents(text):
    """Replace tone marks with tone numbers."""

    if search('[0-9¹²³⁴⁵⁶⁷⁸⁹]', text):
        return text

    def _deaccentuate(p):
        return (
            p.group(1) +
            base_letters[p.group(2).lower()] +
            p.group(3) +
            get_tone_number(p.group(2).lower())
        )

    return sub(
        '([a-zü]*)([' + 'aeiouüvAEIOUÜV' + accents + '])([a-zü]*)',
        _deaccentuate,
        text,
        flags=IGNORECASE
    )


def separate(pinyin, grouped=True):
    """Separate pinyin syllables.

    Example: "Yīlù píng'ān" => "Yī lù píng ān"
    """

    def _clean(t):
        if t.startswith("'"):
            return t[1:]
        return t

    def _separate(p):
        return _clean(p.group('one')) + ' ' + _clean(p.group('two'))

    transcription = config_manager.options['transcription']

    separated = []
    for text in pinyin.split():
        if transcription in ['Pinyin', 'Pinyin (Taiwan)']:
            text = pinyin_two_re.sub(_separate, text)
            text = pinyin_two_re.sub(_separate, text)

        if transcription in ['Cantonese']:
            text = jyutping_two_re.sub(_separate, text)
            text = jyutping_two_re.sub(_separate, text)

        if grouped:
            separated.append(text)
        else:
            separated.extend(text.split())

    return separated


def get_tone_number(pinyin):
    if match(r".+1[0-9]$", pinyin):
        return pinyin[-2:]
    elif match(r".+[0-9]$", pinyin):
        return pinyin[-1:]
    elif match(".+[¹²³⁴]$", pinyin):
        return str(" ¹²³⁴".index(pinyin[-1:]))
    elif match("[\u3100-\u312F]", pinyin):#Bopomofo
        if match("[ˊˇˋ˙]", pinyin[-1:]):
            return str("  ˊˇˋ˙".index(pinyin[-1:]))
        else:
            return "1"
    else:
        for c in pinyin:
            try:
                return str(vowel_tone_dict[c])
            except KeyError:
                continue
        return "5"


def no_tone(text):
    """Remove tone information and coloring."""

    from .color import no_color

    text = no_color(text)
    text = no_accents(text)

    def _remove_tone_number(p):
        return p.group(1) + sub(r'1?[0-9¹²³⁴]', '', p.group(2)) + ']'

    if has_ruby(text):
        return sub(r'([\u3400-\u9fff]\[)([^[]+?)\]', _remove_tone_number, text)

    return sub(r'([a-zü]+)1?[0-9¹²³⁴]', r'\1', text)
