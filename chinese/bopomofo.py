# -*- coding: utf-8 -*-
#
# Copyright © 2012 Thomas TEMPÉ, <thomas.tempe@alysse.org>
# 
# DWTHYW license.
# Do what the fuck you want with this file.
#
# Data taken from the excellent tables at
# http://www.yellowbridge.com/chinese/zhuyin.php
import re

initials_re = "([BPMFDTNLGKHJQXRZCS]|ZH|CH|SH)"
medials_re = "(YI|WU|YU|[IUVU]|)"
finals_re = "(YE|AI|EI|AO|OU|ANG|ENG|AN|EN|ER|[AOE]|)"
tones_re = "([1-5]?)"

initials_dict = {
"B":u"ㄅ","P":u"ㄆ","M":u"ㄇ","F":u"ㄈ",
"D":u"ㄉ","T":u"ㄊ","N":u"ㄋ","L":u"ㄌ",
"G":u"ㄍ","K":u"ㄎ","H":u"ㄏ",
"J":u"ㄐ","Q":u"ㄑ","X":u"ㄒ",
"ZH":u"ㄓ","CH":u"ㄔ","SH":u"ㄕ","R":u"ㄖ",
"Z":u"ㄗ","C":u"ㄘ","S":u"ㄙ"}

medials_dict = {
"I":u"ㄧ","YI":u"ㄧ",
"U":u"ㄨ","WU":u"ㄨ",
"V":u"ㄩ","YU":u"ㄩ"}

finals_dict = {
"A":u"ㄚ","O":u"ㄛ","E":u"ㄜ","E":u"ㄝ","YE":u"ㄝ",
"AI":u"ㄞ","EI":u"ㄟ","AO":u"ㄠ","OU":u"ㄡ",
"AN":u"ㄢ","EN":u"ㄣ","ANG":u"ㄤ","ENG":u"ㄥ","ER":u"ㄦ"}

tones_dict = {
 "1":"", "2":u"ˊ", "3":u"ˇ","4":u"ˋ", "5":u"˙"}

def bopomofo_sub(p):
    r = initials_dict[p.group(1)]
    try:
        r += medials_dict[p.group(2)]
    except:
        pass
    try:
        r +=  finals_dict[p.group(3)]
    except:
        pass
    try:
        r +=  tones_dict[p.group(4)]
    except:
        pass
    return r

def bopomofo(pinyin):
    '''Convert a pinyin string to Bopomofo
    The optional tone info must be given as a number suffix, eg: 'ni3'
    '''
    pinyin = pinyin.upper()
    return re.sub(initials_re+medials_re+finals_re+tones_re, bopomofo_sub, pinyin)

