# -*- coding: utf-8 -*-
# Copyright 2012-2015 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017 Luo Li-Yan <joseph.lorimer13@gmail.com>

# You can read about all available functions at:
# https://github.com/ttempe/chinese-support-addon/wiki/Edit-behavior
# Also, see the Python tutorial at http://docs.python.org/2/tutorial

from aqt import mw

from .config import chinese_support_config as config
from .edit_functions import (accentuate_pinyin,
                             cleanup,
                             colorize,
                             colorize_fuse,
                             get_alternate_spellings,
                             get_any,
                             get_mean_word,
                             has_field,
                             hide,
                             hide_ruby,
                             no_color,
                             no_sound,
                             no_tone,
                             pinyin_to_bopomofo,
                             ruby,
                             separate_pinyin,
                             setAll,
                             silhouette,
                             simplify,
                             sound,
                             traditional,
                             transcribe,
                             translate)


def get_mean(hanzi, dico):
    mw = get_mean_word(hanzi)
    if mw:
        # If there's no mean word field, then add it here
        if not has_field(config.options['fields']['classifier'], dico):
            return '<br>Cl: ' + mw
        # Otherwise add it to the mean word field
        elif get_any(config.options['fields']['classifier'], dico) == '':
            setAll(config.options['fields']['classifier'], dico, to=mw)
    return ''


def get_alt(hanzi, dico):
    alt = get_alternate_spellings(hanzi)
    if alt:
        # If there's no alt spelling field, then add it here
        if not has_field(config.options['fields']['alternative'], dico):
            return '<br>Also written: ' + alt
        # Otherwise add it to the alt spelling field
        elif get_any(config.options['fields']['alternative'], dico) == '':
            setAll(config.options['fields']['alternative'], dico, to=alt)
    return ''


# Returns 1 if a translation was found in the dictionary, otherwise returns 0
def update_Meaning_fields(hanzi, dico):
    mw = get_mean(hanzi, dico)
    alt = get_alt(hanzi, dico)

    # Update Meaning field only if empty
    m = ''
    if get_any(config.options['fields']['meaning'], dico) == '':
        m = translate(hanzi)
        if not m:  # Translation is empty
            return 0
        m = m + mw + alt
        setAll(config.options['fields']['meaning'], dico, to=m)

    return 1


def update_English_fields(hanzi, dico):
    mw = get_mean(hanzi, dico)
    alt = get_alt(hanzi, dico)

    m = ''
    if get_any(config.options['fields']['english'], dico) == '':
        m = translate(hanzi, 'zh', 'local_en')
        if not m:  # Translation is empty
            return 0
        m = m + mw + alt
        setAll(config.options['fields']['english'], dico, to=m)

    return 1


def update_German_fields(hanzi, dico):
    mw = get_mean(hanzi, dico)
    alt = get_alt(hanzi, dico)

    m = ''
    if get_any(config.options['fields']['german'], dico) == '':
        m = translate(hanzi, 'zh', 'local_de')
        if not m:  # Translation is empty
            return 0
        m = m + mw + alt
        setAll(config.options['fields']['german'], dico, to=m)

    return 1


def update_French_fields(hanzi, dico):
    mw = get_mean(hanzi, dico)
    alt = get_alt(hanzi, dico)

    m = ''
    if get_any(config.options['fields']['french'], dico) == '':
        m = translate(hanzi, 'zh', 'local_fr')
        if not m:  # Translation is empty
            return 0
        m = m + mw + alt
        setAll(config.options['fields']['french'], dico, to=m)

    return 1


def update_all_Meaning_fields(hanzi, dico):
    update_Meaning_fields(hanzi, dico)
    update_English_fields(hanzi, dico)
    update_German_fields(hanzi, dico)
    update_French_fields(hanzi, dico)


def update_Silhouette_fields(hanzi, dico):
    m = silhouette(hanzi)
    setAll(config.options['fields']['silhouette'], dico, to=m)


def format_Transcription_fields(dico):
    t = colorize(
        accentuate_pinyin(
            separate_pinyin(
                cleanup(get_any(config.options['fields']['transcription'], dico)))))
    t = hide(t, no_tone(t))
    setAll(config.options['fields']['transcription'], dico, to=t)


# Returns 1 if pinyin was added, otherwise returns 0
def update_Transcription_fields(hanzi, dico):
    # Only if it's empty
    if get_any(config.options['fields']['transcription'], dico) == '':
        t = colorize(transcribe(no_sound(hanzi)))
        # Hide the unaccented transcription in the field, to make searching
        # easier
        t = hide(t, no_tone(t))
        setAll(config.options['fields']['transcription'], dico, to=t)
        return 1
    # Otherwise colorize and accentuate the existing pinyin
    else:
        format_Transcription_fields(dico)
        return 0


def format_Pinyin_fields(dico):
    t = colorize(accentuate_pinyin(separate_pinyin(cleanup(
        get_any(config.options['fields']['pinyin'], dico)), True), True))
    t = hide(t, no_tone(t))
    setAll(config.options['fields']['pinyin'], dico, to=t)


def update_Pinyin_fields(hanzi, dico):
    if get_any(config.options['fields']['pinyin'], dico) == '':
        t = colorize(transcribe(no_sound(hanzi), 'Pinyin'))
        t = hide(t, no_tone(t))
        setAll(config.options['fields']['pinyin'], dico, to=t)
        return 1
    else:
        format_Pinyin_fields(dico)
        return 0


def format_PinyinTW_fields(dico):
    t = colorize(accentuate_pinyin(separate_pinyin(cleanup(
        get_any(config.options['fields']['pinyinTaiwan'], dico)), True), True))
    t = hide(t, no_tone(t))
    setAll(config.options['fields']['pinyinTaiwan'], dico, to=t)

    # Also update Bopomofo
    if has_field(config.options['fields']['bopomofo'], dico):
        setAll(config.options['fields']['bopomofo'], dico, to=pinyin_to_bopomofo(t))


def update_PinyinTW_fields(hanzi, dico):
    if get_any(config.options['fields']['pinyinTaiwan'], dico) == '':
        t = colorize(transcribe(no_sound(hanzi), 'Pinyin (Taiwan)'))
        t = hide(t, no_tone(t))
        setAll(config.options['fields']['pinyinTaiwan'], dico, to=t)
        return 1
    else:
        format_PinyinTW_fields(dico)
        return 0


def format_Cantonese_fields(dico):
    t = colorize(
        separate_pinyin(
            cleanup(get_any(config.options['fields']['cantonese'], dico)), True, True))
    t = hide(t, no_tone(t))
    setAll(config.options['fields']['cantonese'], dico, to=t)


def update_Cantonese_fields(hanzi, dico):
    if get_any(config.options['fields']['cantonese'], dico) == '':
        t = colorize(transcribe(no_sound(hanzi), 'Cantonese', False))
        t = hide(t, no_tone(t))
        setAll(config.options['fields']['cantonese'], dico, to=t)
        return 1
    else:
        format_Cantonese_fields(dico)
        return 0


def format_Bopomofo_fields(dico):
    t = colorize(cleanup(get_any(config.options['fields']['bopomofo'], dico)))
    t = hide(t, no_tone(t))
    setAll(config.options['fields']['bopomofo'], dico, to=t)


def update_Bopomofo_fields(hanzi, dico):
    if get_any(config.options['fields']['bopomofo'], dico) == '':
        t = colorize(transcribe(no_sound(hanzi), 'Bopomofo'))
        t = hide(t, no_tone(t))
        setAll(config.options['fields']['bopomofo'], dico, to=t)
        return 1
    else:
        format_Bopomofo_fields(dico)
        return 0


def update_all_Transcription_fields(hanzi, dico):
    update_Transcription_fields(hanzi, dico)
    update_Pinyin_fields(hanzi, dico)
    update_PinyinTW_fields(hanzi, dico)
    update_Cantonese_fields(hanzi, dico)
    update_Bopomofo_fields(hanzi, dico)


def update_Color_fields(hanzi, dico):
    # Update Color fields from the Hanzi field,
    h = no_sound(hanzi)

    # Take the tone info from the Transcription, Pinyin, PinyinTW, Cantonese or
    # Bopomofo field
    if has_field(config.options['fields']['transcription'], dico):
        t = no_sound(no_color(get_any(config.options['fields']['transcription'], dico)))
    elif has_field(config.options['fields']['pinyin'], dico):
        t = no_sound(no_color(get_any(config.options['fields']['pinyin'], dico)))
    elif has_field(config.options['fields']['pinyinTaiwan'], dico):
        t = no_sound(no_color(get_any(config.options['fields']['pinyinTaiwan'], dico)))
    elif has_field(config.options['fields']['cantonese'], dico):
        t = no_sound(no_color(get_any(config.options['fields']['cantonese'], dico)))
    elif has_field(config.options['fields']['bopomofo'], dico):
        t = no_sound(no_color(get_any(config.options['fields']['bopomofo'], dico)))
    else:
        t = ''
    c = colorize_fuse(h, t)
    setAll(config.options['fields']['color'], dico, to=c)


def update_ColorPY_fields(hanzi, dico):
    # Update Color fields from the Hanzi field,
    h = no_sound(hanzi)

    # Take the tone info from the Pinyin field
    t = no_sound(no_color(get_any(config.options['fields']['pinyin'], dico)))
    c = colorize_fuse(h, t)
    setAll(config.options['fields']['colorPinyin'], dico, to=c)


def update_ColorPYTW_fields(hanzi, dico):
    # Update Color fields from the Hanzi field,
    h = no_sound(hanzi)

    # Take the tone info from the PinyinTW field
    t = no_sound(no_color(get_any(config.options['fields']['pinyinTaiwan'], dico)))
    c = colorize_fuse(h, t)
    setAll(config.options['fields']['colorPinyinTaiwan'], dico, to=c)


def update_ColorCANT_fields(hanzi, dico):
    # Update Color fields from the Hanzi field,
    h = no_sound(hanzi)

    # Take the tone info from the Cantonese field
    t = no_sound(no_color(get_any(config.options['fields']['cantonese'], dico)))
    c = colorize_fuse(h, t)
    setAll(config.options['fields']['colorCantonese'], dico, to=c)


def update_ColorBPMF_fields(hanzi, dico):
    # Update Color fields from the Hanzi field,
    h = no_sound(hanzi)

    # Take the tone info from the Bopomofo field
    t = no_sound(no_color(get_any(config.options['fields']['bopomofo'], dico)))
    c = colorize_fuse(h, t)
    setAll(config.options['fields']['colorBopomofo'], dico, to=c)


def update_all_Color_fields(hanzi, dico):
    update_Color_fields(hanzi, dico)
    update_ColorPY_fields(hanzi, dico)
    update_ColorPYTW_fields(hanzi, dico)
    update_ColorCANT_fields(hanzi, dico)
    update_ColorBPMF_fields(hanzi, dico)


# Returns 1 if a sound was added, otherwise returns 0
def update_Sound_fields(hanzi, dico):
    # Update Sound field from Hanzi field if non-empty (only if field actually
    # exists, as it implies downloading a soundfile from Internet)
    if (has_field(config.options['fields']['sound'], dico) and
            get_any(config.options['fields']['sound'], dico) == ''):
        s = sound(hanzi)
        if s:
            setAll(config.options['fields']['sound'], dico, to=s)
            return 1, 0  # 1 field filled, 0 errors
        return 0, 1
    return 0, 0


def update_Sound_Mandarin_fields(hanzi, dico):
    # Update Sound field from Hanzi field if non-empty (only if field actually
    # exists, as it implies downloading a soundfile from Internet)
    if (has_field(config.options['fields']['mandarinSound'], dico) and
            get_any(config.options['fields']['mandarinSound'], dico) == ''):
        s = sound(hanzi, 'Google TTS Mandarin')
        if s:
            setAll(config.options['fields']['mandarinSound'], dico, to=s)
            return 1, 0  # 1 field filled, 0 errors
        return 0, 1
    return 0, 0


def update_Sound_Cantonese_fields(hanzi, dico):
    # Update Sound field from Hanzi field if non-empty (only if field actually
    # exists, as it implies downloading a soundfile from Internet)
    if (has_field(config.options['fields']['cantoneseSound'], dico) and
            get_any(config.options['fields']['cantoneseSound'], dico) == ''):
        s = sound(hanzi, 'Google TTS Cantonese')
        if s:
            setAll(config.options['fields']['cantoneseSound'], dico, to=s)
            return 1, 0  # 1 field filled, 0 errors
        return 0, 1
    return 0, 0


def update_all_Sound_fields(hanzi, dico):
    updated1, errors1 = update_Sound_fields(hanzi, dico)
    updated2, errors2 = update_Sound_Mandarin_fields(hanzi, dico)
    updated3, errors3 = update_Sound_Cantonese_fields(hanzi, dico)
    return updated1+updated2+updated3, errors1+errors2+errors3


def update_Simplified_fields(hanzi, dico):
    # Don't do anything if already filled
    if not get_any(config.options['fields']['simplified'], dico) == '':
        return

    s = simplify(hanzi)
    if s != hanzi:
        setAll(config.options['fields']['simplified'], dico, to=s)
    else:
        setAll(config.options['fields']['simplified'], dico, to='')


def update_Traditional_fields(hanzi, dico):
    # Don't do anything if already filled
    if not get_any(config.options['fields']['traditional'], dico) == '':
        return

    t = traditional(hanzi)
    if t != hanzi:
        setAll(config.options['fields']['traditional'], dico, to=t)
    else:
        setAll(config.options['fields']['traditional'], dico, to='')


def update_Ruby_fields(hanzi, dico):
    # Ruby field will fill as long as either a Transcription, Pinyin, PinyinTW,
    # Cantonese or Bopomofo field exists
    if has_field(config.options['fields']['transcription'], dico):
        m = colorize_fuse(
            hanzi, get_any(config.options['fields']['transcription'], dico), ruby=True)
    elif has_field(config.options['fields']['pinyin'], dico):
        m = colorize_fuse(
            hanzi, get_any(config.options['fields']['pinyin'], dico), ruby=True)
    elif has_field(config.options['fields']['pinyinTaiwan'], dico):
        m = colorize_fuse(
            hanzi, get_any(config.options['fields']['pinyinTaiwan'], dico), ruby=True)
    elif has_field(config.options['fields']['cantonese'], dico):
        m = colorize_fuse(
            hanzi, get_any(config.options['fields']['cantonese'], dico), ruby=True)
    elif has_field(config.options['fields']['bopomofo'], dico):
        m = colorize_fuse(
            hanzi, get_any(config.options['fields']['bopomofo'], dico), ruby=True)
    else:
        m = ''
    setAll(config.options['fields']['ruby'], dico, to=m)


def update_RubyPY_fields(hanzi, dico):
    m = colorize_fuse(
        hanzi, get_any(config.options['fields']['pinyin'], dico), ruby=True)
    setAll(config.options['fields']['rubyPinyin'], dico, to=m)


def update_RubyPYTW_fields(hanzi, dico):
    m = colorize_fuse(
        hanzi, get_any(config.options['fields']['pinyinTaiwan'], dico), ruby=True)
    setAll(config.options['fields']['rubyPinyinTaiwan'], dico, to=m)


def update_RubyCANT_fields(hanzi, dico):
    m = colorize_fuse(
        hanzi, get_any(config.options['fields']['cantonese'], dico), ruby=True)
    setAll(config.options['fields']['rubyCantonese'], dico, to=m)


def update_RubyBPMF_fields(hanzi, dico):
    m = colorize_fuse(
        hanzi, get_any(config.options['fields']['bopomofo'], dico), ruby=True)
    setAll(config.options['fields']['rubyBopomofo'], dico, to=m)


def update_all_Ruby_fields(hanzi, dico):
    update_Ruby_fields(hanzi, dico)
    update_RubyPY_fields(hanzi, dico)
    update_RubyPYTW_fields(hanzi, dico)
    update_RubyCANT_fields(hanzi, dico)
    update_RubyBPMF_fields(hanzi, dico)


def eraseFields(note):
    for fields in config.options['fields'].values():
        setAll(fields, note, to='')


def updateFields(note, currentField, fieldNames):
    if 'addon' in note.model():
        modelType = note.model()['addon']
    else:
        modelType = None

    fieldsCopy = dict(note)

    if modelType == 'Chinese Ruby':
        if currentField == 'Hanzi':
            # Update the ruby
            h = colorize(ruby(accentuate_pinyin(fieldsCopy['Hanzi'])))
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
                ruby(accentuate_pinyin(fieldsCopy[currentField])))
    elif currentField in config.options['fields']['hanzi']:
        if fieldsCopy[currentField]:
            update_all_Meaning_fields(fieldsCopy[currentField], fieldsCopy)
            update_all_Transcription_fields(
                fieldsCopy[currentField], fieldsCopy)
            update_all_Color_fields(fieldsCopy[currentField], fieldsCopy)
            update_all_Sound_fields(fieldsCopy[currentField], fieldsCopy)
            update_Simplified_fields(fieldsCopy[currentField], fieldsCopy)
            update_Traditional_fields(fieldsCopy[currentField], fieldsCopy)
            update_all_Ruby_fields(fieldsCopy[currentField], fieldsCopy)
            update_Silhouette_fields(fieldsCopy[currentField], fieldsCopy)
        else:
            eraseFields(fieldsCopy)
    elif currentField in config.options['fields']['transcription']:
        hanzi = get_any(config.options['fields']['hanzi'], fieldsCopy)
        format_Transcription_fields(fieldsCopy)
        update_all_Color_fields(hanzi, fieldsCopy)
        update_all_Ruby_fields(hanzi, fieldsCopy)
    elif currentField in config.options['fields']['pinyin']:
        hanzi = get_any(config.options['fields']['hanzi'], fieldsCopy)
        format_Pinyin_fields(fieldsCopy)
        update_all_Color_fields(hanzi, fieldsCopy)
        update_all_Ruby_fields(hanzi, fieldsCopy)
    elif currentField in config.options['fields']['pinyinTaiwan']:
        hanzi = get_any(config.options['fields']['hanzi'], fieldsCopy)
        format_PinyinTW_fields(fieldsCopy)
        update_all_Color_fields(hanzi, fieldsCopy)
        update_all_Ruby_fields(hanzi, fieldsCopy)
    elif currentField in config.options['fields']['cantonese']:
        hanzi = get_any(config.options['fields']['hanzi'], fieldsCopy)
        format_Cantonese_fields(fieldsCopy)
        update_all_Color_fields(hanzi, fieldsCopy)
        update_all_Ruby_fields(hanzi, fieldsCopy)
    elif currentField in config.options['fields']['bopomofo']:
        hanzi = get_any(config.options['fields']['hanzi'], fieldsCopy)
        format_Bopomofo_fields(fieldsCopy)
        update_all_Color_fields(hanzi, fieldsCopy)
        update_all_Ruby_fields(hanzi, fieldsCopy)

    updated = False

    for f in fieldNames:
        if note[f] != fieldsCopy[f]:
            note[f] = fieldsCopy[f]
            updated = True

    return updated
