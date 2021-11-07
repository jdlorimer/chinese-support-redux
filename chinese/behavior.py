# Copyright © 2012-2015 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2020 Joseph Lorimer <joseph@lorimer.me>
# Copyright © 2020 Joe Minicucci <https://joeminicucci.com>
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
from .freq import get_frequency
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
    has_any_field,
    hide,
    set_all,
)


def get_classifier(hanzi, note):
    cs = dictionary.get_classifiers(hanzi)
    text = ', '.join(colorize_dict(c) for c in cs)
    if text and not has_any_field(config['fields']['classifier'], note):
        return '<br>Cl: ' + text
    return ''


def fill_classifier(hanzi, note):
    cs = dictionary.get_classifiers(hanzi)
    text = ', '.join(colorize_dict(c) for c in cs)
    filled = False
    if text and has_any_field(config['fields']['classifier'], note):
        set_all(config['fields']['classifier'], note, to=text)
        filled = True
    return filled


def get_alt(hanzi, note):
    alts = dictionary.get_variants(hanzi)
    alt = ', '.join(colorize_dict(a) for a in alts)
    if alt:
        if not has_any_field(config['fields']['alternative'], note):
            return '<br>Also written: ' + alt
        if get_first(config['fields']['alternative'], note) == '':
            set_all(config['fields']['alternative'], note, to=alt)
    return ''


def fill_def(hanzi, note, lang):
    classifier = get_classifier(hanzi, note)
    alt = get_alt(hanzi, note)
    field = {'en': 'english', 'de': 'german', 'fr': 'french'}[lang]
    filled = False

    if not has_any_field(config['fields'][field], note):
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


def fill_usage(hanzi, note):
    filled = False

    if not 'usage' in config['fields']:
        return filled

    if not has_any_field(config['fields']['usage'], note):
        return filled

    if get_first(config['fields']['usage'], note) == '':
        sentences = dictionary.get_sentences(hanzi)
        if sentences:
            numberOfSentences = config.get_config_scalar_value("max_examples")
            if numberOfSentences == -1:
                sentenceList = [sentence.replace('\n', '\n<br>')
                                for sentence in
                                sentences[0].split('\n\n')]
            else:
                sentenceList = [sentence.replace('\n', '\n<br>')
                                for sentence in
                                sentences[0].split('\n\n')[:numberOfSentences]]
            sentences = str.join('\n<br>\n<br>', sentenceList)
            set_all(config['fields']['usage'], note, to=sentences)
            filled = True

    return filled


def fill_transcript(hanzi, note):
    n_filled = 0
    separated = split_hanzi(hanzi)

    for key, target, type_ in [
        ('bopomofo', 'bopomofo', 'trad'),
        ('cantonese', 'jyutping', 'trad'),
        ('pinyin', 'pinyin', 'simp'),
        ('pinyinTaiwan', 'pinyin_tw', 'trad'),
    ]:
        if get_first(config['fields'][key], note) == '':
            trans = colorize(transcribe(separated, target, type_), target)
            trans = hide(trans, no_tone(trans))
            set_all(config['fields'][key], note, to=trans)
            n_filled += 1
        else:
            reformat_transcript(note, key, target)

    return n_filled


def reformat_transcript(note, group, target):
    if target == 'bopomofo':
        return

    transcript = get_first(config['fields'][group], note)
    if transcript is None:
        return

    clean = cleanup(transcript)
    split = split_transcript(clean, target, grouped=True)
    accent = accentuate(split, target)
    color = colorize(accent)
    hidden = hide(color, no_tone(color))

    set_all(config['fields'][group], note, to=hidden)


def fill_color(hanzi, note):
    if config['target'] in ['pinyin', 'pinyin_tw', 'bopomofo']:
        target = 'pinyin'
        field_group = 'pinyin'
    elif config['target'] in 'jyutping':
        target = 'jyutping'
        field_group = 'jyutping'
    else:
        raise NotImplementedError(config['target'])

    #hanziColor
    field = get_first(config['fields'][field_group], note)
    trans = sanitize_transcript(field, target, grouped=False)
    trans = split_transcript(' '.join(trans), target, grouped=False)
    hanzi = split_hanzi(cleanup(hanzi), grouped=False)
    colorized = colorize_fuse(hanzi, trans)
    set_all(config['fields']['colorHanzi'], note, to=colorized)

    #traditional color
    tradHanzi = get_first(config['fields']['traditional'], note)
    if tradHanzi:
        tradHanzi = split_hanzi(cleanup(tradHanzi), grouped=False)
        colorized = colorize_fuse(tradHanzi, trans)
        set_all(config['fields']['colorTraditional'], note, to=colorized)

    #cantonese color
    cantoField = get_first(config['fields']['cantonese'], note)
    if cantoField:
        hanzi = tradHanzi if tradHanzi else hanzi
        cantoTrans = sanitize_transcript(cantoField, "jyutping", grouped=False)
        colorized = colorize_fuse(hanzi, cantoTrans)
        set_all(config['fields']['colorCantonese'], note, to=colorized)


def fill_sound(hanzi, note):
    updated = 0
    errors = 0
    for f in config['fields']['sound'] + config['fields']['mandarinSound']:
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


def fill_frequency(hanzi, note) -> bool:
    if get_first(config['fields']['frequency'], note) == '':
        set_all(
            config['fields']['frequency'],
            note,
            to=get_frequency(get_simp(hanzi)),
        )
        return True

    return False


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
        if has_any_field(config['fields'][trans_group], note):
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
    hanzi = get_first(config['fields']['hanzi'], copy)
    if not hanzi:
        return False
    hanzi = cleanup(hanzi)

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
            fill_trad(hanzi, copy)
            fill_color(hanzi, copy)
            fill_sound(hanzi, copy)
            fill_simp(hanzi, copy)
            fill_frequency(hanzi, copy)
            fill_all_rubies(hanzi, copy)
            fill_silhouette(hanzi, copy)
            fill_usage(hanzi, copy)
        else:
            erase_fields(copy, config.get_fields())
    elif focus_field in config['fields']['pinyin']:
        reformat_transcript(copy, 'pinyin', 'pinyin')
    elif focus_field in config['fields']['pinyinTaiwan']:
        reformat_transcript(copy, 'pinyinTaiwan', 'pinyin_tw')
    elif focus_field in config['fields']['cantonese']:
        reformat_transcript(copy, 'cantonese', 'jyutping')

    updated = False

    for f in fields:
        if note[f] != copy[f]:
            note[f] = copy[f]
            updated = True

    return updated
