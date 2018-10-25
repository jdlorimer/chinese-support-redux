# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from re import DOTALL, sub


def has_field(fields, d):
    """Return true if any of the fields are available.

    Case-insensitive.
    """
    for k in d:
        for f in fields:
            try:
                if str(f.lower()) == str(k.lower()):
                    return True
            except:
                pass
    return False


def get_any(fields, d):
    """Return contents of first available field from list.

    Case-insensitive.
    """
    for f in fields:
        for k in d:
            try:
                if str(f.lower()) == str(k.lower()):
                    return d[k]
            except:
                pass
    return ''


def set_all(fields, note, to):
    fields = [f.lower() for f in fields]

    for f in note.keys():
        if f.lower() in fields:
            note[f] = to


def cleanup(text):
    if not text:
        return str()
    text = no_html(text)
    text = text.replace('&nbsp;', ' ')
    text = sub(r'^\s*', '', text)
    text = sub(r'\s*$', '', text)
    # cloze
    text = sub(r'\{\{c[0-9]+::(.*?)(::.*?)?\}\}', r'\1', text)
    return text


def no_html(text):
    return sub(r'<.*?>', '', text, flags=DOTALL)


def hide(text, hidden):
    """Add hidden keyword to string.

    For searching purposes.
    """
    from .color import no_color

    if not text or text == '<br />':
        return ''

    hidden = no_color(hidden)
    hidden = hidden.replace(r'<.*?>', '')
    hidden = hidden.replace(r'[<!->]', '')

    return text + '<!--' + hidden + '-->'


def no_hidden(text):
    return sub(r'<!--.*?-->', '', text)


def add_with_space(a, b):
    if a and not a.endswith(' '):
        return a + ' ' + b
    return a + b
