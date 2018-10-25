# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from re import IGNORECASE, sub

from .consts import accents
from .hanzi import has_hanzi
from .util import cleanup, no_hidden
from .sound import extract_sound_tags


def colorize(words, ruby_whole=False):
    """Add tone color info. Works on transcription, hanzi or ruby.

    Note: Can be seen in the card preview, but not the note edit view.

    In the case of ruby, it will colorize only the annotation by default.
    If ruby_whole = True, then it will colorize the whole character.

    Warning: it's not recommended to use this function on hanzi directly,
    since it cannot choose the correct color in the case of 多音字."""

    from .ruby import has_ruby
    from .transcribe import get_tone_number, transcribe

    def colorize_ruby_sub(p):
        return '<span class="tone{t}">{r}</span>'.format(
            t=get_tone_number(p.group(2)),
            r=p.group()
        )

    def colorize_hanzi_sub(p):
        return '<span class="tone{t}">{r}</span>'.format(
            t=get_tone_number(transcribe(p.group(1), only_one=True)),
            r=p.group()
        )

    def colorize_pinyin_sub(text, pattern):
        def repl(p):
            if p.group()[0] in '&<"/':
                return p.group()
            return '<span class="tone{t}">{r}</span>'.format(
                t=get_tone_number(p.group(1)),
                r=p.group()
            )

        return sub(pattern, repl, text, IGNORECASE).replace('> <', '><')

    whole_ruby_pattern = (
        r'([\u3400-\u9fff]\[\s*)([a-zü' +
        accents +
        r']+1?[0-9¹²³⁴]?)(.*?\])'
    )
    half_ruby_pattern = r'([a-zü' + accents + r']+1?[0-9¹²³⁴]?)'
    hanzi_pattern = r'([\u3400-\u9fff])'
    pinyin_pattern = (
        r'([&<"/]?[a-zü\u3100-\u312F' +
        accents +
        r']+1?[0-9¹²³⁴ˊˇˋ˙]?)'
    )

    colorized = []
    for text in words:
        text = no_color(text)
        (text, sound_tags) = extract_sound_tags(text)

        if has_ruby(text):
            if ruby_whole:
                text = sub(
                    whole_ruby_pattern,
                    colorize_ruby_sub,
                    text,
                    flags=IGNORECASE
                )
            else:
                text = colorize_pinyin_sub(text, half_ruby_pattern)
        elif has_hanzi(text):
            text = sub(hanzi_pattern, colorize_hanzi_sub, text)
        else:
            text = colorize_pinyin_sub(text, pinyin_pattern)

        colorized.append(text + sound_tags)

    return ' '.join(colorized)


def colorize_fuse(hanzi, pinyin, ruby=False):
    """Colorize hanzi based on pinyin tone.

    If ruby=True, then annotate hanzi with pinyin.
    """

    from .transcribe import get_tone_number, separate

    standard_fmt = '<span class="tone{tone}">{hanzi}</span>'
    ruby_fmt = '<span class="tone{tone}"><ruby>{hanzi}<rt>{pinyin}</rt></span>'

    hanzi = [h for h in cleanup(hanzi)]

    pinyin = ' '.join(
        separate(cleanup(no_color(pinyin)), grouped=False)
    ).split()

    text = ''

    for h, p in zip(hanzi, pinyin):
        if ruby:
            text += ruby_fmt.format(tone=get_tone_number(p), hanzi=h, pinyin=p)
        else:
            text += standard_fmt.format(tone=get_tone_number(p), hanzi=h)

    return text


def local_dict_colorize(txt, ruby=True):
    """
    Colorize text in the form:
    "Hello is written 你好[ni3 hao]"
    (as used in the local dictionaries)
    """

    from .transcribe import accentuate, separate

    def _sub(p):
        c = ''
        hanzi = p.group(1)
        pinyin = p.group(2)
        pinyin = ' '.join(accentuate(separate(pinyin)))
        delimiter = '|'

        if hanzi.count(delimiter) == 1:
            hanzi = hanzi.split(delimiter)
            c += colorize_fuse(hanzi[0], pinyin, True)
            c += delimiter
            c += colorize_fuse(hanzi[1], pinyin, False)
        else:
            c += colorize_fuse(hanzi, pinyin, False)

        if not ruby:
            c += '[' + colorize(separate(pinyin)) + ']'

        return c

    txt = sub(r'([\u3400-\u9fff|]+)\[(.*?)\]', _sub, txt)
    return txt


def no_color(text):
    "Remove tone color info and other HTML pollutions"
    if not text:
        return ''
    text = text.replace(r'&nbsp;', '')
    text = no_hidden(text)
    text = sub(r'<span class="tone1?[0-9]">(.*?)</span>', r'\1', text)
    # sometimes added by Anki
    text = sub(r'<font color="#000000">(.*?)</font>', r'\1', text)
    # pinyin toolkit coloring
    text = sub(r'<span style=.*?>(.*?)</span>', r'\1', text)
    return text
