# -*- coding: utf-8 -*-
# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2014 Alex Griffin <alex@alexjgriffin.com>
# Copyright 2017 Joseph Lorimer <luoliyan@posteo.net>
# License: DWTFYW

# early replacements
replacements = [
    ('jue', 'ㄐㄩㄝ'),
    ('lue', 'ㄌㄩㄝ'),
    ('nue', 'ㄋㄩㄝ'),
    ('que', 'ㄑㄩㄝ'),
    ('v', 'u:'),
    ('w', 'u'),
    ('wong', 'ㄨㄥ'),
    ('wu', 'u'),
    ('xue', 'ㄒㄩㄝ'),
    ('y', 'i'),
    ('yi', 'i'),
    ('you', 'ㄧㄡ'),
    ('yu', 'u:'),
    ('yue', 'ㄩㄝ'),
    ('ü', 'u:'),
]

special = [
    ('chi', 'ㄔ'),
    ('ci', 'ㄘ'),
    ('ju', 'ㄐㄩ'),
    ('qu', 'ㄑㄩ'),
    ('r5', 'ㄦ'),
    ('ri', 'ㄖ'),
    ('shi', 'ㄕ'),
    ('si', 'ㄙ'),
    ('xu', 'ㄒㄩ'),
    ('zhi', 'ㄓ'),
    ('zi', 'ㄗ'),
]

initials = [
    ('b', 'ㄅ'),
    ('c', 'ㄘ'),
    ('ch', 'ㄔ'),
    ('d', 'ㄉ'),
    ('f', 'ㄈ'),
    ('g', 'ㄍ'),
    ('h', 'ㄏ'),
    ('j', 'ㄐ'),
    ('k', 'ㄎ'),
    ('l', 'ㄌ'),
    ('m', 'ㄇ'),
    ('n', 'ㄋ'),
    ('p', 'ㄆ'),
    ('q', 'ㄑ'),
    ('r', 'ㄖ'),
    ('s', 'ㄙ'),
    ('sh', 'ㄕ'),
    ('t', 'ㄊ'),
    ('x', 'ㄒ'),
    ('z', 'ㄗ'),
    ('zh', 'ㄓ'),
]

finals = [
    ('a', 'ㄚ'),
    ('ai', 'ㄞ'),
    ('an', 'ㄢ'),
    ('ang', 'ㄤ'),
    ('ao', 'ㄠ'),
    ('e', 'ㄜ'),
    ('ei', 'ㄟ'),
    ('en', 'ㄣ'),
    ('eng', 'ㄥ'),
    ('er', 'ㄦ'),
    ('i', 'ㄧ'),
    ('ia', 'ㄧㄚ'),
    ('iai', 'ㄧㄞ'),
    ('ian', 'ㄧㄢ'),
    ('iang', 'ㄧㄤ'),
    ('iao', 'ㄧㄠ'),
    ('ie', 'ㄧㄝ'),
    ('in', 'ㄧㄣ'),
    ('ing', 'ㄧㄥ'),
    ('io', 'ㄧㄛ'),
    ('iong', 'ㄩㄥ'),
    ('iu', 'ㄧㄡ'),
    ('o', 'ㄛ'),
    ('ong', 'ㄨㄥ'),
    ('ou', 'ㄡ'),
    ('u', 'ㄨ'),
    ('u:', 'ㄩ'),
    ('u:an', 'ㄩㄢ'),
    ('u:e', 'ㄩㄝ'),
    ('u:n', 'ㄩㄣ'),
    ('ua', 'ㄨㄚ'),
    ('uai', 'ㄨㄞ'),
    ('uan', 'ㄨㄢ'),
    ('uang', 'ㄨㄤ'),
    ('ui', 'ㄨㄟ'),
    ('un', 'ㄨㄣ'),
    ('uo', 'ㄨㄛ'),
    ('ê', 'ㄝ'),
]

tones = [
    ('1', ''),
    ('2', 'ˊ'),
    ('3', 'ˇ'),
    ('4', 'ˋ'),
    ('5', '˙')
]

table = special + initials + finals + tones
table.sort(key=lambda pair: len(pair[0]), reverse=True)
replacements.extend(table)


def bopomofo(pinyin):
    '''Convert a pinyin string to Bopomofo
    The optional tone info must be given as a number suffix, eg: 'ni3'
    '''
    pinyin = pinyin.lower()

    for (a, b) in replacements:
        pinyin = pinyin.replace(a, b)

    return pinyin
