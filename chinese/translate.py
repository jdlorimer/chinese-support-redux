# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from .color import local_dict_colorize
from .main import config_manager, dictionary
from .util import cleanup


def translate_local(text, lang):
    """Translate using local dictionary.

    lang is one of 'en', 'fr', 'de', 'es'.
    """

    defs = dictionary.get_definitions(text, lang)

    if not defs:
        return ''

    def multiple_pinyins(defs):
        prev_p, _, _, _ = defs[0]
        for pinyin, _, _, _ in defs:
            if pinyin != prev_p:
                return True
        return False

    res = ''

    for pinyin, definition, _, _ in defs:
        if multiple_pinyins(defs):
            res += '❖ %s[%s] %s\n' % (text, pinyin, definition)
        else:
            res += ' \t' + definition + '\n'

    res = res.replace('\n', '\n<br>')

    return local_dict_colorize(res)


def translate(text, to_lang=None):
    """Translate to a different language.

    Example: '你好' becomes 'hello'

    to_lang is one of 'local_en', 'local_de', 'local_fr'.

    If to_lang is unspecified, the default language will be used.
    """

    text = cleanup(text)
    if not text:
        return ''
    if not to_lang:
        to_lang = config_manager.options['dictionary']
        if to_lang == 'None':
            return ''
    if to_lang.startswith('local_'):  # local dictionary
        return translate_local(text, to_lang[-2:])


def get_alternate_spellings(text):
    if not text:
        return ''
    alt = dictionary.get_alt_spellings(text)
    if list(alt):
        return local_dict_colorize(', '.join(alt))
    return ''
