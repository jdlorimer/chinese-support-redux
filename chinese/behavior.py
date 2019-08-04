# Copyright © 2012-2015 Thomas TEMPÉ <thomas.tempe@alysse.org>
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

from .color import colorize, colorize_dict, colorize_fuse
from .freq import lookup_frequency
from .hanzi import get_silhouette, get_simp, get_trad, split_hanzi
from .main import config, dictionary
from .sound import sound
from .transcribe import (
    accentuate,
    no_tone,
    sanitize_transcript,
    split_transcript,
    transcribe,
)
from .translate import translate
from .util import (
    cleanup,
    erase_fields,
    flatten,
    get_first,
    has_field,
    hide,
    set_all,
)


def get_classifier(hanzi, note):
    cs = dictionary.get_classifiers(hanzi)
    text = ', '.join(colorize_dict(c) for c in cs)
    if text and not has_field(config['fields']['classifier'], note):
        return '<br>Cl: ' + text
    return ''


def fill_classifier(hanzi, note):
    cs = dictionary.get_classifiers(hanzi)
    text = ', '.join(colorize_dict(c) for c in cs)
    filled = False
    if text and has_field(config['fields']['classifier'], note):
        set_all(config['fields']['classifier'], note, to=text)
        filled = True
    return filled


def get_alt(hanzi, note):
    alts = dictionary.get_variants(hanzi)
    alt = ', '.join(colorize_dict(a) for a in alts)
    if alt:
        if not has_field(config['fields']['alternative'], note):
            return '<br>Also written: ' + alt
        if get_first(config['fields']['alternative'], note) == '':
            set_all(config['fields']['alternative'], note, to=alt)
    return ''


def fill_def(hanzi, note, lang):
    classifier = get_classifier(hanzi, note)
    alt = get_alt(hanzi, note)
    field = {'en': 'english', 'de': 'german', 'fr': 'french'}[lang]
    filled = False

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
            fill_def(hanzi, note, lang='en'),
            fill_def(hanzi, note, lang='de'),
            fill_def(hanzi, note, lang='fr'),
        ]
    )
    return n_filled


def fill_silhouette(hanzi, note):
    m = get_silhouette(hanzi)
    set_all(config['fields']['silhouette'], note, to=m)


def fill_transcript(hanzi, note):
    n_filled = 0
    separated = split_hanzi(hanzi)

    for key, target, func, type_ in [
        ('pinyin', 'pinyin', format_pinyin, 'simp'),
        ('pinyinTaiwan', 'pinyin_tw', format_taiwan_pinyin, 'trad'),
        ('cantonese', 'jyutping', format_cantonese, 'trad'),
    ]:
        if get_first(config['fields'][key], note) == '':
            trans = colorize(transcribe(separated, target, type_))
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
            split_transcript(
                cleanup(get_first(config['fields']['pinyin'], note)),
                'pinyin',
                grouped=True,
            ),
            'pinyin',
        )
    )
    t = hide(t, no_tone(t))
    set_all(config['fields']['pinyin'], note, to=t)


def format_taiwan_pinyin(note):
    t = colorize(
        accentuate(
            split_transcript(
                cleanup(get_first(config['fields']['pinyinTaiwan'], note)),
                'pinyin',
                grouped=True,
            ),
            'pinyin',
        )
    )
    t = hide(t, no_tone(t))
    set_all(config['fields']['pinyinTaiwan'], note, to=t)


def format_cantonese(note):
    t = colorize(
        split_transcript(
            cleanup(get_first(config['fields']['cantonese'], note)),
            'jyutping',
            grouped=True,
        )
    )
    t = hide(t, no_tone(t))
    set_all(config['fields']['cantonese'], note, to=t)


def fill_bopomofo(hanzi, note):
    field = get_first(config['fields']['bopomofo'], note)

    if field:
        syllables = cleanup(field).split()
        n_filled = 0
    else:
        syllables = transcribe(split_hanzi(hanzi), 'bopomofo', 'trad')
        n_filled = 1

    text = colorize(syllables)
    text = hide(text, no_tone(text))
    set_all(config['fields']['bopomofo'], note, to=text)

    return n_filled


def fill_color(hanzi, note):
    if config['target'] in ['pinyin', 'pinyin_tw', 'bopomofo']:
        target = 'pinyin'
        field_group = 'pinyin'
    elif config['target'] in 'jyutping':
        target = 'jyutping'
        field_group = 'jyutping'
    else:
        raise NotImplementedError(config['target'])

    field = get_first(config['fields'][field_group], note)
    trans = sanitize_transcript(field, target, grouped=False)
    trans = split_transcript(' '.join(trans), target, grouped=False)
    hanzi = split_hanzi(cleanup(hanzi), grouped=False)
    colorized = colorize_fuse(hanzi, trans)
    set_all(config['fields']['colorHanzi'], note, to=colorized)


def fill_sound(hanzi, note):
    updated = 0
    errors = 0
    for f in config['fields']['mandarinSound']:
        if f in note and note[f] == '':
            s = sound(hanzi, config['speech'])
            if s:
                note[f] = s
                updated += 1
            else:
                errors += 1
    return updated, errors


def fill_simp(hanzi, note):
    if not get_first(config['fields']['simplified'], note) == '':
        return

    s = get_simp(hanzi)
    if s is not None and s != hanzi:
        set_all(config['fields']['simplified'], note, to=s)
    else:
        set_all(config['fields']['simplified'], note, to='')


def fill_trad(hanzi, note):
    if not get_first(config['fields']['traditional'], note) == '':
        return

    t = get_trad(hanzi)
    if t is not None and t != hanzi:
        set_all(config['fields']['traditional'], note, to=t)
    else:
        set_all(config['fields']['traditional'], note, to='')


def fill_frequency(hanzi, note):
    if not get_first(config['fields']['frequency'], note) == '':
        return

    s = get_simp(hanzi)
    f = lookup_frequency(s)
    set_all(config['fields']['frequency'], note, to=f)


def fill_ruby(hanzi, note, trans_group, ruby_group):
    if trans_group == 'bopomofo':
        trans = flatten(
            s.split()
            for s in transcribe(
                split_hanzi(hanzi, grouped=True), 'bopomofo', 'trad'
            )
        )
    elif trans_group in ['pinyin', 'pinyinTaiwan']:
        field = get_first(config['fields'][trans_group], note)
        trans = sanitize_transcript(field, 'pinyin', grouped=False)
    elif trans_group == 'cantonese':
        field = get_first(config['fields'][trans_group], note)
        trans = sanitize_transcript(field, 'jyutping', grouped=False)
    else:
        raise NotImplementedError(trans_group)

    hanzi = split_hanzi(cleanup(hanzi), grouped=False)
    rubified = colorize_fuse(hanzi, trans, ruby=True)
    set_all(config['fields'][ruby_group], note, to=rubified)


def fill_all_rubies(hanzi, note):
    for trans_group in ['pinyin', 'pinyinTaiwan', 'cantonese', 'bopomofo']:
        if has_field(config['fields'][trans_group], note):
            fill_ruby(hanzi, note, trans_group, 'ruby')
            break

    for trans_group, ruby_group in [
        ('pinyin', 'rubyPinyin'),
        ('pinyinTaiwan', 'rubyPinyinTaiwan'),
        ('cantonese', 'rubyCantonese'),
        ('bopomofo', 'rubyBopomofo'),
    ]:
        fill_ruby(hanzi, note, trans_group, ruby_group)


def update_fields(note, focus_field, fields):
    copy = dict(note)
    hanzi = cleanup(get_first(config['fields']['hanzi'], copy))

    transcript_fields = (
        config['fields']['pinyin']
        + config['fields']['pinyinTaiwan']
        + config['fields']['cantonese']
        + config['fields']['bopomofo']
    )

    if focus_field in transcript_fields:
        fill_color(hanzi, copy)
        fill_all_rubies(hanzi, copy)

    if focus_field in config['fields']['hanzi']:
        if copy[focus_field]:
            fill_all_defs(hanzi, copy)
            fill_classifier(hanzi, copy)
            fill_transcript(hanzi, copy)
            fill_color(hanzi, copy)
            fill_sound(hanzi, copy)
            fill_simp(hanzi, copy)
            fill_trad(hanzi, copy)
            fill_frequency(hanzi, copy)
            fill_all_rubies(hanzi, copy)
            fill_silhouette(hanzi, copy)
        else:
            erase_fields(copy)
    elif focus_field in config['fields']['pinyin']:
        format_pinyin(copy)
    elif focus_field in config['fields']['pinyinTaiwan']:
        format_taiwan_pinyin(copy)
    elif focus_field in config['fields']['cantonese']:
        format_cantonese(copy)

    updated = False

    for f in fields:
        if note[f] != copy[f]:
            note[f] = copy[f]
            updated = True

    return updated
