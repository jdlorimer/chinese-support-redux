# Copyright © 2012-2015 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
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
from .hanzi import silhouette, simplify, traditional
from .main import config, dictionary
from .ruby import hide_ruby, ruby
from .sound import no_sound, sound
from .transcribe import accentuate, no_tone, separate_trans, transcribe
from .translate import translate
from .util import cleanup, get_first, has_field, hide, no_color, set_all


def get_classifier(hanzi, d):
    cs = dictionary.get_classifiers(hanzi)
    text = ', '.join(colorize_dict(c) for c in cs)
    if text and not has_field(config['fields']['classifier'], d):
        return '<br>Cl: ' + text
    return ''


def fill_classifier(hanzi, d):
    cs = dictionary.get_classifiers(hanzi)
    text = ', '.join(colorize_dict(c) for c in cs)
    if text and has_field(config['fields']['classifier'], d):
        set_all(config['fields']['classifier'], d, to=text)


def get_alt(hanzi, d):
    alts = dictionary.get_alt_spellings(hanzi)
    alt = ', '.join(colorize_dict(a) for a in alts)
    if alt:
        if not has_field(config['fields']['alternative'], d):
            return '<br>Also written: ' + alt
        if get_first(config['fields']['alternative'], d) == '':
            set_all(config['fields']['alternative'], d, to=alt)
    return ''


def fill_definition(hanzi, note, lang=None):
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


def fill_all_definitions(hanzi, note):
    n_filled = sum(
        [
            fill_definition(hanzi, note),
            fill_definition(hanzi, note, lang='en'),
            fill_definition(hanzi, note, lang='de'),
            fill_definition(hanzi, note, lang='fr'),
        ]
    )
    fill_classifier(hanzi, note)
    return n_filled


def update_Silhouette_fields(hanzi, d):
    m = silhouette(hanzi)
    set_all(config['fields']['silhouette'], d, to=m)


def format_Transcription_fields(d):
    t = colorize(
        accentuate(
            separate_trans(
                cleanup(get_first(config['fields']['transcription'], d))
            )
        )
    )
    t = hide(t, no_tone(t))
    set_all(config['fields']['transcription'], d, to=t)


def fill_transcription(hanzi, note):
    if get_first(config['fields']['transcription'], note) == '':
        trans = colorize(transcribe([no_sound(hanzi)]))
        trans = hide(trans, no_tone(trans))
        set_all(config['fields']['transcription'], note, to=trans)
        return 1

    format_Transcription_fields(note)
    return 0


def format_Pinyin_fields(d):
    t = colorize(
        accentuate(
            separate_trans(
                cleanup(get_first(config['fields']['pinyin'], d)), True
            )
        )
    )
    t = hide(t, no_tone(t))
    set_all(config['fields']['pinyin'], d, to=t)


def fill_pinyin(hanzi, note):
    if get_first(config['fields']['pinyin'], note) == '':
        t = colorize(transcribe([no_sound(hanzi)], 'Pinyin'))
        t = hide(t, no_tone(t))
        set_all(config['fields']['pinyin'], note, to=t)
        return 1
    format_Pinyin_fields(note)
    return 0


def format_PinyinTW_fields(d):
    t = colorize(
        accentuate(
            separate_trans(
                cleanup(get_first(config['fields']['pinyinTaiwan'], d)), True
            )
        )
    )
    t = hide(t, no_tone(t))
    set_all(config['fields']['pinyinTaiwan'], d, to=t)

    if has_field(config['fields']['bopomofo'], d):
        set_all(config['fields']['bopomofo'], d, to=bopomofo(t))


def update_PinyinTW_fields(hanzi, d):
    if get_first(config['fields']['pinyinTaiwan'], d) == '':
        t = colorize(transcribe([no_sound(hanzi)], 'Pinyin (Taiwan)'))
        t = hide(t, no_tone(t))
        set_all(config['fields']['pinyinTaiwan'], d, to=t)
        return 1
    else:
        format_PinyinTW_fields(d)
        return 0


def format_Cantonese_fields(d):
    t = colorize(
        separate_trans(cleanup(get_first(config['fields']['cantonese'], d)))
    )
    t = hide(t, no_tone(t))
    set_all(config['fields']['cantonese'], d, to=t)


def update_Cantonese_fields(hanzi, d):
    if get_first(config['fields']['cantonese'], d) == '':
        t = colorize(transcribe([no_sound(hanzi)], 'Cantonese', False))
        t = hide(t, no_tone(t))
        set_all(config['fields']['cantonese'], d, to=t)
        return 1
    else:
        format_Cantonese_fields(d)
        return 0


def update_bopomofo(hanzi, d):
    field = get_first(config['fields']['bopomofo'], d)

    if field:
        syllables = no_color(cleanup(field)).split()
        n_added = 0
    else:
        syllables = transcribe(list(no_sound(hanzi)), 'Bopomofo')
        n_added = 1

    text = colorize(syllables)
    text = hide(text, no_tone(text))
    set_all(config['fields']['bopomofo'], d, to=text)

    return n_added


def fill_all_transcriptions(hanzi, note):
    fill_transcription(hanzi, note)
    fill_pinyin(hanzi, note)
    update_PinyinTW_fields(hanzi, note)
    update_Cantonese_fields(hanzi, note)
    update_bopomofo(hanzi, note)


def fill_color(hanzi, d):
    h = no_sound(hanzi)

    # get tone from transcription field
    if has_field(config['fields']['transcription'], d):
        t = no_sound(no_color(get_first(config['fields']['transcription'], d)))
    elif has_field(config['fields']['pinyin'], d):
        t = no_sound(no_color(get_first(config['fields']['pinyin'], d)))
    elif has_field(config['fields']['pinyinTaiwan'], d):
        t = no_sound(no_color(get_first(config['fields']['pinyinTaiwan'], d)))
    elif has_field(config['fields']['cantonese'], d):
        t = no_sound(no_color(get_first(config['fields']['cantonese'], d)))
    elif has_field(config['fields']['bopomofo'], d):
        t = no_sound(no_color(get_first(config['fields']['bopomofo'], d)))
    else:
        t = ''

    c = colorize_fuse(h, t)
    set_all(config['fields']['color'], d, to=c)


def update_ColorPY_fields(hanzi, d):
    h = no_sound(hanzi)
    t = no_sound(no_color(get_first(config['fields']['pinyin'], d)))
    c = colorize_fuse(h, t)
    set_all(config['fields']['colorPinyin'], d, to=c)


def update_ColorPYTW_fields(hanzi, d):
    h = no_sound(hanzi)
    t = no_sound(no_color(get_first(config['fields']['pinyinTaiwan'], d)))
    c = colorize_fuse(h, t)
    set_all(config['fields']['colorPinyinTaiwan'], d, to=c)


def update_ColorCANT_fields(hanzi, d):
    h = no_sound(hanzi)
    t = no_sound(no_color(get_first(config['fields']['cantonese'], d)))
    c = colorize_fuse(h, t)
    set_all(config['fields']['colorCantonese'], d, to=c)


def update_ColorBPMF_fields(hanzi, d):
    h = no_sound(hanzi)
    t = no_sound(no_color(get_first(config['fields']['bopomofo'], d)))
    c = colorize_fuse(h, t)
    set_all(config['fields']['colorBopomofo'], d, to=c)


def update_all_Color_fields(hanzi, d):
    fill_color(hanzi, d)
    update_ColorPY_fields(hanzi, d)
    update_ColorPYTW_fields(hanzi, d)
    update_ColorCANT_fields(hanzi, d)
    update_ColorBPMF_fields(hanzi, d)


# Returns 1 if a sound was added, otherwise returns 0
def update_Sound_fields(hanzi, d):
    # Update Sound field from Hanzi field if non-empty (only if field actually
    # exists, as it implies downloading a soundfile from Internet)
    if (
        has_field(config['fields']['sound'], d)
        and get_first(config['fields']['sound'], d) == ''
    ):
        s = sound(hanzi)
        if s:
            set_all(config['fields']['sound'], d, to=s)
            return 1, 0  # 1 field filled, 0 errors
        return 0, 1
    return 0, 0


def update_Sound_Mandarin_fields(hanzi, d):
    # Update Sound field from Hanzi field if non-empty (only if field actually
    # exists, as it implies downloading a soundfile from Internet)
    if (
        has_field(config['fields']['mandarinSound'], d)
        and get_first(config['fields']['mandarinSound'], d) == ''
    ):
        s = sound(hanzi, 'Google TTS Mandarin')
        if s:
            set_all(config['fields']['mandarinSound'], d, to=s)
            return 1, 0  # 1 field filled, 0 errors
        return 0, 1
    return 0, 0


def update_Sound_Cantonese_fields(hanzi, d):
    # Update Sound field from Hanzi field if non-empty (only if field actually
    # exists, as it implies downloading a soundfile from Internet)
    if (
        has_field(config['fields']['cantoneseSound'], d)
        and get_first(config['fields']['cantoneseSound'], d) == ''
    ):
        s = sound(hanzi, 'Google TTS Cantonese')
        if s:
            set_all(config['fields']['cantoneseSound'], d, to=s)
            return 1, 0  # 1 field filled, 0 errors
        return 0, 1
    return 0, 0


def update_all_Sound_fields(hanzi, d):
    updated1, errors1 = update_Sound_fields(hanzi, d)
    updated2, errors2 = update_Sound_Mandarin_fields(hanzi, d)
    updated3, errors3 = update_Sound_Cantonese_fields(hanzi, d)
    return updated1 + updated2 + updated3, errors1 + errors2 + errors3


def update_Simplified_fields(hanzi, d):
    if not get_first(config['fields']['simplified'], d) == '':
        return

    s = simplify(hanzi)
    if s != hanzi:
        set_all(config['fields']['simplified'], d, to=s)
    else:
        set_all(config['fields']['simplified'], d, to='')


def update_Traditional_fields(hanzi, d):
    if not get_first(config['fields']['traditional'], d) == '':
        return

    t = traditional(hanzi)
    if t != hanzi:
        set_all(config['fields']['traditional'], d, to=t)
    else:
        set_all(config['fields']['traditional'], d, to='')


def update_Ruby_fields(hanzi, d):
    # Ruby field will fill as long as either a Transcription, Pinyin, PinyinTW
    # Cantonese or Bopomofo field exists
    if has_field(config['fields']['transcription'], d):
        m = colorize_fuse(
            hanzi, get_first(config['fields']['transcription'], d), ruby=True
        )
    elif has_field(config['fields']['pinyin'], d):
        m = colorize_fuse(
            hanzi, get_first(config['fields']['pinyin'], d), ruby=True
        )
    elif has_field(config['fields']['pinyinTaiwan'], d):
        m = colorize_fuse(
            hanzi, get_first(config['fields']['pinyinTaiwan'], d), ruby=True
        )
    elif has_field(config['fields']['cantonese'], d):
        m = colorize_fuse(
            hanzi, get_first(config['fields']['cantonese'], d), ruby=True
        )
    elif has_field(config['fields']['bopomofo'], d):
        m = colorize_fuse(
            hanzi, get_first(config['fields']['bopomofo'], d), ruby=True
        )
    else:
        m = ''
    set_all(config['fields']['ruby'], d, to=m)


def update_RubyPY_fields(hanzi, d):
    m = colorize_fuse(
        hanzi, get_first(config['fields']['pinyin'], d), ruby=True
    )
    set_all(config['fields']['rubyPinyin'], d, to=m)


def update_RubyPYTW_fields(hanzi, d):
    m = colorize_fuse(
        hanzi, get_first(config['fields']['pinyinTaiwan'], d), ruby=True
    )
    set_all(config['fields']['rubyPinyinTaiwan'], d, to=m)


def update_RubyCANT_fields(hanzi, d):
    m = colorize_fuse(
        hanzi, get_first(config['fields']['cantonese'], d), ruby=True
    )
    set_all(config['fields']['rubyCantonese'], d, to=m)


def update_RubyBPMF_fields(hanzi, d):
    m = colorize_fuse(
        hanzi, get_first(config['fields']['bopomofo'], d), ruby=True
    )
    set_all(config['fields']['rubyBopomofo'], d, to=m)


def update_all_Ruby_fields(hanzi, d):
    update_Ruby_fields(hanzi, d)
    update_RubyPY_fields(hanzi, d)
    update_RubyPYTW_fields(hanzi, d)
    update_RubyCANT_fields(hanzi, d)
    update_RubyBPMF_fields(hanzi, d)


def eraseFields(note):
    for fields in config['fields'].values():
        set_all(fields, note, to='')


def updateFields(note, currentField, fieldNames):
    if 'addon' in note.model():
        modelType = note.model()['addon']
    else:
        modelType = None

    fieldsCopy = dict(note)
    hanzi = cleanup(get_first(config['fields']['hanzi'], fieldsCopy))

    if modelType == 'Chinese Ruby':
        if currentField == 'Hanzi':
            h = colorize(ruby(accentuate(fieldsCopy['Hanzi'])))
            h = hide_ruby(h)
            fieldsCopy['Hanzi'] = h
            if fieldsCopy['Hanzi'] == '':
                fieldsCopy['Meaning'] = ''
            elif fieldsCopy['Meaning'] == '':
                fieldsCopy['Meaning'] = translate(
                    fieldsCopy['Hanzi'], config['dictionary']
                )
        elif currentField[0:5] == 'Hanzi':
            fieldsCopy[currentField] = colorize(
                ruby(accentuate(fieldsCopy[currentField]))
            )
    elif currentField in config['fields']['hanzi']:
        if fieldsCopy[currentField]:
            fill_all_definitions(hanzi, fieldsCopy)
            fill_all_transcriptions(hanzi, fieldsCopy)
            update_all_Color_fields(hanzi, fieldsCopy)
            update_all_Sound_fields(hanzi, fieldsCopy)
            update_Simplified_fields(hanzi, fieldsCopy)
            update_Traditional_fields(hanzi, fieldsCopy)
            update_all_Ruby_fields(hanzi, fieldsCopy)
            update_Silhouette_fields(hanzi, fieldsCopy)
        else:
            eraseFields(fieldsCopy)
    elif currentField in config['fields']['transcription']:
        format_Transcription_fields(fieldsCopy)
        update_all_Color_fields(hanzi, fieldsCopy)
        update_all_Ruby_fields(hanzi, fieldsCopy)
    elif currentField in config['fields']['pinyin']:
        format_Pinyin_fields(fieldsCopy)
        update_all_Color_fields(hanzi, fieldsCopy)
        update_all_Ruby_fields(hanzi, fieldsCopy)
    elif currentField in config['fields']['pinyinTaiwan']:
        format_PinyinTW_fields(fieldsCopy)
        update_all_Color_fields(hanzi, fieldsCopy)
        update_all_Ruby_fields(hanzi, fieldsCopy)
    elif currentField in config['fields']['cantonese']:
        format_Cantonese_fields(fieldsCopy)
        update_all_Color_fields(hanzi, fieldsCopy)
        update_all_Ruby_fields(hanzi, fieldsCopy)
    elif currentField in config['fields']['bopomofo']:
        # format_bopomofo_fields(fieldsCopy)
        update_all_Color_fields(hanzi, fieldsCopy)
        update_all_Ruby_fields(hanzi, fieldsCopy)

    updated = False

    for f in fieldNames:
        if note[f] != fieldsCopy[f]:
            note[f] = fieldsCopy[f]
            updated = True

    return updated
