# Copyright © 2012-2015 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2019 Joseph Lorimer <luoliyan@posteo.net>
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

from .bopomofo import bopomofo
from .color import colorize, colorize_dict, colorize_fuse
from .hanzi import separate_chars, silhouette, simplify, traditional
from .main import config, dictionary
from .ruby import hide_ruby, ruby
from .sound import no_sound, sound
from .transcribe import accentuate, no_tone, separate_trans, transcribe
from .translate import translate
from .util import cleanup, get_first, has_field, hide, set_all


def get_classifier(hanzi, note):
    cs = dictionary.get_classifiers(hanzi)
    text = ', '.join(colorize_dict(c) for c in cs)
    if text and not has_field(config['fields']['classifier'], note):
        return '<br>Cl: ' + text
    return ''


def fill_classifier(hanzi, note):
    cs = dictionary.get_classifiers(hanzi)
    text = ', '.join(colorize_dict(c) for c in cs)
    if text and has_field(config['fields']['classifier'], note):
        set_all(config['fields']['classifier'], note, to=text)


def get_alt(hanzi, note):
    alts = dictionary.get_alt_spellings(hanzi)
    alt = ', '.join(colorize_dict(a) for a in alts)
    if alt:
        if not has_field(config['fields']['alternative'], note):
            return '<br>Also written: ' + alt
        if get_first(config['fields']['alternative'], note) == '':
            set_all(config['fields']['alternative'], note, to=alt)
    return ''


def fill_def(hanzi, note, lang=None):
    classifier = get_classifier(hanzi, note)
    alt = get_alt(hanzi, note)

    d = {'en': 'english', 'de': 'german', 'fr': 'french'}

    filled = False

    if lang:
        field = d[lang]
    else:
        lang = config['dictionary']
        field = 'meaning'

    if not has_field(config['fields'][field], note):
        return filled

    definition = ''
    if get_first(config['fields'][field], note) == '':
        definition = translate(hanzi, lang)
        if definition:
            definition += classifier + alt
            set_all(config['fields'][field], note, to=definition)
            filled = True

    return filled


def fill_all_defs(hanzi, note):
    n_filled = sum(
        [
            fill_def(hanzi, note),
            fill_def(hanzi, note, lang='en'),
            fill_def(hanzi, note, lang='de'),
            fill_def(hanzi, note, lang='fr'),
        ]
    )
    fill_classifier(hanzi, note)
    return n_filled


def fill_silhouette(hanzi, note):
    m = silhouette(hanzi)
    set_all(config['fields']['silhouette'], note, to=m)


def format_transcription(note):
    t = colorize(
        accentuate(
            separate_trans(
                cleanup(get_first(config['fields']['transcription'], note))
            )
        )
    )
    t = hide(t, no_tone(t))
    set_all(config['fields']['transcription'], note, to=t)


def fill_transcription(hanzi, note):
    n_filled = 0
    separated = separate_chars(hanzi)

    for key, target, func, only_one in [
        ('transcription', None, format_transcription, True),
        ('pinyin', 'Pinyin', format_pinyin, True),
        ('pinyinTaiwan', 'Pinyin (Taiwan)', format_taiwan_pinyin, True),
        ('cantonese', 'Cantonese', format_cantonese, False),
    ]:
        if get_first(config['fields'][key], note) == '':
            trans = colorize(transcribe(separated, target, only_one))
            trans = hide(trans, no_tone(trans))
            set_all(config['fields'][key], note, to=trans)
            n_filled += 1
        else:
            func(note)

    n_filled += fill_bopomofo(hanzi, note)
    return n_filled


def format_pinyin(note):
    t = colorize(
        accentuate(
            separate_trans(
                cleanup(get_first(config['fields']['pinyin'], note)), True
            )
        )
    )
    t = hide(t, no_tone(t))
    set_all(config['fields']['pinyin'], note, to=t)


def format_taiwan_pinyin(note):
    t = colorize(
        accentuate(
            separate_trans(
                cleanup(get_first(config['fields']['pinyinTaiwan'], note)),
                True,
            )
        )
    )
    t = hide(t, no_tone(t))
    set_all(config['fields']['pinyinTaiwan'], note, to=t)


def format_cantonese(note):
    t = colorize(
        separate_trans(cleanup(get_first(config['fields']['cantonese'], note)))
    )
    t = hide(t, no_tone(t))
    set_all(config['fields']['cantonese'], note, to=t)


def fill_bopomofo(hanzi, note):
    field = get_first(config['fields']['bopomofo'], note)

    if field:
        syllables = cleanup(field).split()
        n_filled = 0
    else:
        syllables = transcribe(separate_chars(hanzi), 'Bopomofo')
        n_filled = 1

    text = colorize(syllables)
    text = hide(text, no_tone(text))
    set_all(config['fields']['bopomofo'], note, to=text)

    return n_filled


def fill_color(hanzi, note):
    trans = get_first(config['fields']['transcription'], note)
    trans = no_sound(trans)
    colorized = colorize_fuse(hanzi, trans)
    set_all(config['fields']['color'], note, to=colorized)


def fill_sound(hanzi, note):
    updated = 0
    errors = 0

    for field_group, tts_engine in [
        ('sound', None),
        ('mandarinSound', 'Google TTS Mandarin'),
        ('cantoneseSound', 'Google TTS Cantonese'),
    ]:
        field = get_first(config['fields'][field_group], note)
        if field != '':
            continue
        s = sound(hanzi, tts_engine)
        if s:
            set_all(config['fields'][field_group], note, to=s)
            updated += 1
        else:
            errors += 1

    return updated, errors


def fill_simp(hanzi, note):
    if not get_first(config['fields']['simplified'], note) == '':
        return

    s = simplify(hanzi)
    if s is not None and s != hanzi:
        set_all(config['fields']['simplified'], note, to=s)
    else:
        set_all(config['fields']['simplified'], note, to='')


def fill_trad(hanzi, note):
    if not get_first(config['fields']['traditional'], note) == '':
        return

    t = traditional(hanzi)
    if t is not None and t != hanzi:
        set_all(config['fields']['traditional'], note, to=t)
    else:
        set_all(config['fields']['traditional'], note, to='')


def fill_ruby(hanzi, note):
    if has_field(config['fields']['transcription'], note):
        m = colorize_fuse(
            hanzi,
            get_first(config['fields']['transcription'], note),
            ruby=True,
        )
    elif has_field(config['fields']['pinyin'], note):
        m = colorize_fuse(
            hanzi, get_first(config['fields']['pinyin'], note), ruby=True
        )
    elif has_field(config['fields']['pinyinTaiwan'], note):
        m = colorize_fuse(
            hanzi, get_first(config['fields']['pinyinTaiwan'], note), ruby=True
        )
    elif has_field(config['fields']['cantonese'], note):
        m = colorize_fuse(
            hanzi, get_first(config['fields']['cantonese'], note), ruby=True
        )
    elif has_field(config['fields']['bopomofo'], note):
        m = colorize_fuse(
            hanzi, get_first(config['fields']['bopomofo'], note), ruby=True
        )
    else:
        m = ''

    set_all(config['fields']['ruby'], note, to=m)


def fill_all_rubies(hanzi, note):
    fill_ruby(hanzi, note)

    for trans_field, ruby_field in [
        ('pinyin', 'rubyPinyin'),
        ('pinyinTaiwan', 'rubyPinyinTaiwan'),
        ('cantonese', 'rubyCantonese'),
        ('bopomofo', 'rubyBopomofo'),
    ]:
        rubified = colorize_fuse(
            hanzi, get_first(config['fields'][trans_field], note), ruby=True
        )
        set_all(config['fields'][ruby_field], note, to=rubified)


def erase_fields(note):
    for f in config['fields'].values():
        set_all(f, note, to='')


def update_fields(note, focus_field, fields):
    if 'addon' in note.model():
        model = note.model()['addon']
    else:
        model = None

    copy = dict(note)
    hanzi = no_sound(cleanup(get_first(config['fields']['hanzi'], copy)))

    if model == 'Chinese Ruby':
        if focus_field == 'Hanzi':
            h = colorize(ruby(accentuate(copy['Hanzi'])))
            h = hide_ruby(h)
            copy['Hanzi'] = h
            if copy['Hanzi'] == '':
                copy['Meaning'] = ''
            elif copy['Meaning'] == '':
                copy['Meaning'] = translate(
                    copy['Hanzi'], config['dictionary']
                )
        elif focus_field[0:5] == 'Hanzi':
            copy[focus_field] = colorize(ruby(accentuate(copy[focus_field])))
    elif focus_field in config['fields']['hanzi']:
        if copy[focus_field]:
            fill_all_defs(hanzi, copy)
            fill_transcription(hanzi, copy)
            fill_color(hanzi, copy)
            fill_sound(hanzi, copy)
            fill_simp(hanzi, copy)
            fill_trad(hanzi, copy)
            fill_all_rubies(hanzi, copy)
            fill_silhouette(hanzi, copy)
        else:
            erase_fields(copy)
    elif focus_field in config['fields']['transcription']:
        format_transcription(copy)
        fill_color(hanzi, copy)
        fill_all_rubies(hanzi, copy)
    elif focus_field in config['fields']['pinyin']:
        format_pinyin(copy)
        fill_color(hanzi, copy)
        fill_all_rubies(hanzi, copy)
    elif focus_field in config['fields']['pinyinTaiwan']:
        format_taiwan_pinyin(copy)
        fill_color(hanzi, copy)
        fill_all_rubies(hanzi, copy)
    elif focus_field in config['fields']['cantonese']:
        format_cantonese(copy)
        fill_color(hanzi, copy)
        fill_all_rubies(hanzi, copy)
    elif focus_field in config['fields']['bopomofo']:
        fill_color(hanzi, copy)
        fill_all_rubies(hanzi, copy)

    updated = False

    for f in fields:
        if note[f] != copy[f]:
            note[f] = copy[f]
            updated = True

    return updated
