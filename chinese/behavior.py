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
from .color import colorize, colorize_fuse, local_dict_colorize
from .hanzi import silhouette, simplify, traditional
from .main import config, dictionary
from .ruby import hide_ruby, ruby
from .sound import no_sound, sound
from .transcribe import accentuate, no_tone, separate, transcribe
from .translate import get_alternate_spellings, translate
from .util import cleanup, get_any, has_field, hide, no_color, set_all


def get_mean(hanzi, d):
    cs = dictionary.get_classifiers(hanzi)
    text = ', '.join(local_dict_colorize(c) for c in cs)
    if text and not has_field(config['fields']['classifier'], d):
        return '<br>Cl: ' + text
    return ''


def set_classifier_fields(hanzi, d):
    cs = dictionary.get_classifiers(hanzi)
    text = ', '.join(local_dict_colorize(c) for c in cs)
    if text and has_field(config['fields']['classifier'], d):
        set_all(config['fields']['classifier'], d, to=text)


def get_alt(hanzi, d):
    alt = get_alternate_spellings(hanzi)
    if alt:
        # If there's no alt spelling field, then add it here
        if not has_field(config['fields']['alternative'], d):
            return '<br>Also written: ' + alt
        # Otherwise add it to the alt spelling field
        elif get_any(config['fields']['alternative'], d) == '':
            set_all(config['fields']['alternative'], d, to=alt)
    return ''


# Returns 1 if a translation was found in the dictionary, otherwise returns 0
def update_Meaning_fields(hanzi, d):
    mw = get_mean(hanzi, d)
    alt = get_alt(hanzi, d)

    # Update Meaning field only if empty
    m = ''
    if get_any(config['fields']['meaning'], d) == '':
        m = translate(hanzi)
        if not m:  # Translation is empty
            return 0
        m = m + mw + alt
        set_all(config['fields']['meaning'], d, to=m)

    return 1


def update_English_fields(hanzi, d):
    mw = get_mean(hanzi, d)
    alt = get_alt(hanzi, d)

    m = ''
    if get_any(config['fields']['english'], d) == '':
        m = translate(hanzi, 'local_en')
        if not m:  # Translation is empty
            return 0
        m = m + mw + alt
        set_all(config['fields']['english'], d, to=m)

    return 1


def update_German_fields(hanzi, d):
    mw = get_mean(hanzi, d)
    alt = get_alt(hanzi, d)

    m = ''
    if get_any(config['fields']['german'], d) == '':
        m = translate(hanzi, 'local_de')
        if not m:  # Translation is empty
            return 0
        m = m + mw + alt
        set_all(config['fields']['german'], d, to=m)

    return 1


def update_French_fields(hanzi, d):
    mw = get_mean(hanzi, d)
    alt = get_alt(hanzi, d)

    m = ''
    if get_any(config['fields']['french'], d) == '':
        m = translate(hanzi, 'local_fr')
        if not m:  # Translation is empty
            return 0
        m = m + mw + alt
        set_all(config['fields']['french'], d, to=m)

    return 1


def update_all_Meaning_fields(hanzi, d):
    update_Meaning_fields(hanzi, d)
    update_English_fields(hanzi, d)
    update_German_fields(hanzi, d)
    update_French_fields(hanzi, d)
    set_classifier_fields(hanzi, d)


def update_Silhouette_fields(hanzi, d):
    m = silhouette(hanzi)
    set_all(config['fields']['silhouette'], d, to=m)


def format_Transcription_fields(d):
    t = colorize(accentuate(separate(
        cleanup(get_any(config['fields']['transcription'], d)))))
    t = hide(t, no_tone(t))
    set_all(config['fields']['transcription'], d, to=t)


# Returns 1 if pinyin was added, otherwise returns 0
def update_Transcription_fields(hanzi, d):
    # Only if it's empty
    if get_any(config['fields']['transcription'], d) == '':
        t = colorize(transcribe(no_sound(hanzi)))
        # Hide the unaccented transcription in the field, to make searching
        # easier
        t = hide(t, no_tone(t))
        set_all(config['fields']['transcription'], d, to=t)
        return 1
    # Otherwise colorize and accentuate the existing pinyin
    else:
        format_Transcription_fields(d)
        return 0


def format_Pinyin_fields(d):
    t = colorize(
        accentuate(
            separate(cleanup(get_any(config['fields']['pinyin'], d))),
            True
        )
    )
    t = hide(t, no_tone(t))
    set_all(config['fields']['pinyin'], d, to=t)


def update_Pinyin_fields(hanzi, d):
    if get_any(config['fields']['pinyin'], d) == '':
        t = colorize(transcribe(no_sound(hanzi), 'Pinyin'))
        t = hide(t, no_tone(t))
        set_all(config['fields']['pinyin'], d, to=t)
        return 1
    format_Pinyin_fields(d)
    return 0


def format_PinyinTW_fields(d):
    t = colorize(accentuate(separate(cleanup(
        get_any(config['fields']['pinyinTaiwan'], d))), True))
    t = hide(t, no_tone(t))
    set_all(config['fields']['pinyinTaiwan'], d, to=t)

    if has_field(config['fields']['bopomofo'], d):
        set_all(config['fields']['bopomofo'], d, to=bopomofo(t))


def update_PinyinTW_fields(hanzi, d):
    if get_any(config['fields']['pinyinTaiwan'], d) == '':
        t = colorize(transcribe(no_sound(hanzi), 'Pinyin (Taiwan)'))
        t = hide(t, no_tone(t))
        set_all(config['fields']['pinyinTaiwan'], d, to=t)
        return 1
    else:
        format_PinyinTW_fields(d)
        return 0


def format_Cantonese_fields(d):
    t = colorize(separate(
            cleanup(get_any(config['fields']['cantonese'], d))))
    t = hide(t, no_tone(t))
    set_all(config['fields']['cantonese'], d, to=t)


def update_Cantonese_fields(hanzi, d):
    if get_any(config['fields']['cantonese'], d) == '':
        t = colorize(transcribe(no_sound(hanzi), 'Cantonese', False))
        t = hide(t, no_tone(t))
        set_all(config['fields']['cantonese'], d, to=t)
        return 1
    else:
        format_Cantonese_fields(d)
        return 0


def update_bopomofo(hanzi, d):
    field = get_any(config['fields']['bopomofo'], d)

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


def update_all_Transcription_fields(hanzi, d):
    update_Transcription_fields(hanzi, d)
    update_Pinyin_fields(hanzi, d)
    update_PinyinTW_fields(hanzi, d)
    update_Cantonese_fields(hanzi, d)
    update_bopomofo(hanzi, d)


def update_Color_fields(hanzi, d):
    # Update Color fields from the Hanzi field
    h = no_sound(hanzi)

    # Take the tone info from the Transcription, Pinyin, PinyinTW, Cantonese or
    # Bopomofo field
    if has_field(config['fields']['transcription'], d):
        t = no_sound(no_color(get_any(config['fields']['transcription'], d)))
    elif has_field(config['fields']['pinyin'], d):
        t = no_sound(no_color(get_any(config['fields']['pinyin'], d)))
    elif has_field(config['fields']['pinyinTaiwan'], d):
        t = no_sound(no_color(get_any(config['fields']['pinyinTaiwan'], d)))
    elif has_field(config['fields']['cantonese'], d):
        t = no_sound(no_color(get_any(config['fields']['cantonese'], d)))
    elif has_field(config['fields']['bopomofo'], d):
        t = no_sound(no_color(get_any(config['fields']['bopomofo'], d)))
    else:
        t = ''
    c = colorize_fuse(h, t)
    set_all(config['fields']['color'], d, to=c)


def update_ColorPY_fields(hanzi, d):
    # Update Color fields from the Hanzi field
    h = no_sound(hanzi)

    # Take the tone info from the Pinyin field
    t = no_sound(no_color(get_any(config['fields']['pinyin'], d)))
    c = colorize_fuse(h, t)
    set_all(config['fields']['colorPinyin'], d, to=c)


def update_ColorPYTW_fields(hanzi, d):
    # Update Color fields from the Hanzi field
    h = no_sound(hanzi)

    # Take the tone info from the PinyinTW field
    t = no_sound(no_color(get_any(config['fields']['pinyinTaiwan'], d)))
    c = colorize_fuse(h, t)
    set_all(config['fields']['colorPinyinTaiwan'], d, to=c)


def update_ColorCANT_fields(hanzi, d):
    # Update Color fields from the Hanzi field
    h = no_sound(hanzi)

    # Take the tone info from the Cantonese field
    t = no_sound(no_color(get_any(config['fields']['cantonese'], d)))
    c = colorize_fuse(h, t)
    set_all(config['fields']['colorCantonese'], d, to=c)


def update_ColorBPMF_fields(hanzi, d):
    # Update Color fields from the Hanzi field
    h = no_sound(hanzi)

    # Take the tone info from the Bopomofo field
    t = no_sound(no_color(get_any(config['fields']['bopomofo'], d)))
    c = colorize_fuse(h, t)
    set_all(config['fields']['colorBopomofo'], d, to=c)


def update_all_Color_fields(hanzi, d):
    update_Color_fields(hanzi, d)
    update_ColorPY_fields(hanzi, d)
    update_ColorPYTW_fields(hanzi, d)
    update_ColorCANT_fields(hanzi, d)
    update_ColorBPMF_fields(hanzi, d)


# Returns 1 if a sound was added, otherwise returns 0
def update_Sound_fields(hanzi, d):
    # Update Sound field from Hanzi field if non-empty (only if field actually
    # exists, as it implies downloading a soundfile from Internet)
    if (has_field(config['fields']['sound'], d) and
            get_any(config['fields']['sound'], d) == ''):
        s = sound(hanzi)
        if s:
            set_all(config['fields']['sound'], d, to=s)
            return 1, 0  # 1 field filled, 0 errors
        return 0, 1
    return 0, 0


def update_Sound_Mandarin_fields(hanzi, d):
    # Update Sound field from Hanzi field if non-empty (only if field actually
    # exists, as it implies downloading a soundfile from Internet)
    if (has_field(config['fields']['mandarinSound'], d) and
            get_any(config['fields']['mandarinSound'], d) == ''):
        s = sound(hanzi, 'Google TTS Mandarin')
        if s:
            set_all(config['fields']['mandarinSound'], d, to=s)
            return 1, 0  # 1 field filled, 0 errors
        return 0, 1
    return 0, 0


def update_Sound_Cantonese_fields(hanzi, d):
    # Update Sound field from Hanzi field if non-empty (only if field actually
    # exists, as it implies downloading a soundfile from Internet)
    if (has_field(config['fields']['cantoneseSound'], d) and
            get_any(config['fields']['cantoneseSound'], d) == ''):
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
    return updated1+updated2+updated3, errors1+errors2+errors3


def update_Simplified_fields(hanzi, d):
    # Don't do anything if already filled
    if not get_any(config['fields']['simplified'], d) == '':
        return

    s = simplify(hanzi)
    if s != hanzi:
        set_all(config['fields']['simplified'], d, to=s)
    else:
        set_all(config['fields']['simplified'], d, to='')


def update_Traditional_fields(hanzi, d):
    # Don't do anything if already filled
    if not get_any(config['fields']['traditional'], d) == '':
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
            hanzi, get_any(config['fields']['transcription'], d), ruby=True)
    elif has_field(config['fields']['pinyin'], d):
        m = colorize_fuse(
            hanzi, get_any(config['fields']['pinyin'], d), ruby=True)
    elif has_field(config['fields']['pinyinTaiwan'], d):
        m = colorize_fuse(
            hanzi, get_any(config['fields']['pinyinTaiwan'], d), ruby=True)
    elif has_field(config['fields']['cantonese'], d):
        m = colorize_fuse(
            hanzi, get_any(config['fields']['cantonese'], d), ruby=True)
    elif has_field(config['fields']['bopomofo'], d):
        m = colorize_fuse(
            hanzi, get_any(config['fields']['bopomofo'], d), ruby=True)
    else:
        m = ''
    set_all(config['fields']['ruby'], d, to=m)


def update_RubyPY_fields(hanzi, d):
    m = colorize_fuse(
        hanzi, get_any(config['fields']['pinyin'], d), ruby=True)
    set_all(config['fields']['rubyPinyin'], d, to=m)


def update_RubyPYTW_fields(hanzi, d):
    m = colorize_fuse(
        hanzi, get_any(config['fields']['pinyinTaiwan'], d), ruby=True)
    set_all(config['fields']['rubyPinyinTaiwan'], d, to=m)


def update_RubyCANT_fields(hanzi, d):
    m = colorize_fuse(
        hanzi, get_any(config['fields']['cantonese'], d), ruby=True)
    set_all(config['fields']['rubyCantonese'], d, to=m)


def update_RubyBPMF_fields(hanzi, d):
    m = colorize_fuse(
        hanzi, get_any(config['fields']['bopomofo'], d), ruby=True)
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
    hanzi = cleanup(get_any(config['fields']['hanzi'], fieldsCopy))

    if modelType == 'Chinese Ruby':
        if currentField == 'Hanzi':
            # Update the ruby
            h = colorize(ruby(accentuate(fieldsCopy['Hanzi'])))
            # Add the toneless transcription and hanzi, hidden, to make them
            # searchable
            h = hide_ruby(h)
            fieldsCopy['Hanzi'] = h
            if fieldsCopy['Hanzi'] == '':
                fieldsCopy['Meaning'] = ''
            elif fieldsCopy['Meaning'] == '':
                fieldsCopy['Meaning'] = translate(fieldsCopy['Hanzi'])
        elif currentField[0:5] == 'Hanzi':
            fieldsCopy[currentField] = colorize(
                ruby(accentuate(fieldsCopy[currentField])))
    elif currentField in config['fields']['hanzi']:
        if fieldsCopy[currentField]:
            update_all_Meaning_fields(hanzi, fieldsCopy)
            update_all_Transcription_fields(hanzi, fieldsCopy)
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
