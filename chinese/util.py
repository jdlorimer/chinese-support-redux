# Copyright © 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2019 Joseph Lorimer <joseph@lorimer.me>
#
# This file is part of Chinese Support Redux.
#
# Chinese Support Redux is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Chinese Support Redux is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Chinese Support Redux.  If not, see <https://www.gnu.org/licenses/>.

from re import DOTALL, sub
from unicodedata import category

from .consts import CLOZE_REGEX


def has_field(field, note):
    for f in note:
        if str(field.lower()) == str(f.lower()):
            return True
    return False


def has_any_field(note, fields):
    for f in fields:
        if has_field(f, note):
            return True
    return False


def all_fields_empty(note, fields):
    for f in fields:
        if note.get(f):
            return False
    return True


def erase_fields(note, fields):
    for f in fields:
        set_all(f, note, to='')


def get_first(fields, note):
    for f in fields:
        for k in note:
            if str(f.lower()) == str(k.lower()):
                return note[k]
    return None


def set_all(fields, note, to):
    fields = [f.lower() for f in fields]

    for f in note.keys():
        if f.lower() in fields:
            note[f] = to


def cleanup(text):
    if text is None:
        raise ValueError(text)
    if not text.strip():
        return ''
    text = no_html(text)
    text = text.replace('&nbsp;', ' ')
    text = sub(r'^\s*', '', text)
    text = sub(r'\s*$', '', text)
    text = sub(CLOZE_REGEX, r'\1', text)
    return text


def no_html(text):
    return sub(r'<.*?>', '', text, flags=DOTALL)


def hide(text, hidden):
    """Add hidden keyword to string to allow search."""

    if not text or text == '<br />':
        return ''

    hidden = no_color(hidden)
    hidden = hidden.replace(r'<.*?>', '')
    hidden = hidden.replace(r'[<!->]', '')

    return '{} <!-- {} -->'.format(text, hidden)


def no_color(text):
    if not text:
        return ''
    text = text.replace(r'&nbsp;', '')
    text = no_hidden(text)
    text = sub(r'<span class="tone1?[0-9]">(.*?)</span>', r'\1', text)
    text = sub(r'<font color="#000000">(.*?)</font>', r'\1', text)
    text = sub(r'<span style=.*?>(.*?)</span>', r'\1', text)
    return text


def no_hidden(text):
    return sub(r' *<!--.*?--> *', ' ', text)


def add_with_space(a, b):
    if a and not a.endswith(' '):
        return a + ' ' + b
    return a + b


def is_punc(s):
    if s is None:
        return False
    return all(category(c).startswith('P') for c in s)


def align(a, b):
    done = []
    i = j = 0
    m = max([len(a), len(b)])
    if a and not b:
        return list(zip(a, [None] * len(a)))
    if not a and b:
        return list(zip([None] * len(b), b))
    if not a and not b:
        return []
    a += [None] * (m - len(a))
    b += [None] * (m - len(b))
    for _ in range(m):
        if (is_punc(a[i]) and is_punc(b[j])) or (
            not is_punc(a[i]) and not is_punc(b[j])
        ):
            done.append((a[i], b[j]))
            i += 1
            j += 1
        elif is_punc(a[i]) and not is_punc(b[j]):
            done.append((a[i], None))
            i += 1
        elif not is_punc(a[i]) and is_punc(b[j]):
            done.append((None, b[j]))
            j += 1
    return done


def save_note(orig, copy):
    n_changed = 0
    for f in orig.keys():
        if f in copy and copy[f] != orig[f]:
            orig[f] = copy[f]
            n_changed += 1
    orig.flush()
    return n_changed


def flatten(a):
    c = []
    for b in a:
        c.extend(b)
    return c
