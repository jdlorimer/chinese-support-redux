# -*- coding: utf-8 -*-
#
# Copyright © 2012 Thomas TEMPÉ, <thomas.tempe@alysse.org>
# 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

import re

from cjklib import characterlookup
from config import chinese_support_config
import translate as translate_module
import bopomofo as bopomofo_module
import google_tts

# Essential Edit functions
##################################################################
#
# You may call any of these functions from the edit_behavior.py file.

def colorize(text, ruby_whole=False):
    u'''Add tone color info.
    (can be seen in the card preview, but not the note edit view).
    Works on transcription, hanzi or ruby.

    In the case of ruby, it will colorize only the annotation by default.
    If ruby_whole = True, then it will colorize the whole character.

    Warning : it's not recommended to use this function on hanzi directly,
    since it cannot choose the correct color in the case of 
    多音字 (characters with multiple pronunciations).'''
    text = no_color(text)
    (text, sound_tags) = extract_sound_tags(text)

    def colorize_hanzi_sub(p):
        return u'<span class="tone{t}">{r}</span>'.format(t=get_tone_number(transcribe(p.group(1), only_one=True)), r=p.group())

    def colorize_pinyin_sub(p):
        return u'<span class="tone{t}">{r}</span>'.format(t=get_tone_number(p.group(1)), r=p.group())


    if has_ruby(text): #Treat like ruby
        if ruby_whole:
            def colorize_ruby_sub(p):
                return u'<span class="tone{t}">{r}</span>'.format(t=get_tone_number(p.group(2)), r=p.group())

            text = re.sub(u'([\u4e00-\u9fff]\[\s*)([a-z'+accents+u']+1?[0-9¹²³⁴]?)(.*?\])', colorize_ruby_sub, text, flags=re.I)    
        else:
            text = re.sub(u'([a-z'+accents+u']+1?[0-9¹²³⁴]?)', colorize_pinyin_sub, text, flags=re.I)
    elif has_hanzi(text):
        text = re.sub(u'([\u4e00-\u9fff])', colorize_hanzi_sub, text)
    else:
        text = re.sub(u'([a-z'+accents+u']+1?[0-9¹²³⁴]?)', colorize_pinyin_sub, text, flags=re.I)
    text = text+sound_tags
    return text

def ruby_top(txt):
    "Extract the top (pronunciation) part of a ruby string."
    r = r' ?([^ >]+?)\[(.+?)\]'
    return re.sub(r, r'\2 ', no_sound(txt))

def ruby_bottom(txt):
    "Extract the bottom part of a ruby string."
    r = r' ?([^ >]+?)\[(.+?)\]'
    return re.sub(r, r'\1 ', no_sound(txt))

def no_color(text):
    "Remove tone color info and other HTML pollutions"
    text = re.sub(r'&nbsp;', '', text)
    text = no_hidden(text)
    #remove color info
    text = re.sub(r'<span class="tone1?[0-9]">(.*?)</span>', r'\1', text)
    return text

def hide(text, hidden):
    """Add hidden keyword to string (typically Hanzi and toneless pinyin),
    to make a note searchable in the 'browse' window
    """
    hidden = no_color(hidden)
    hidden = re.sub(r"[<!->]", "", hidden)
    return text + "<!--"+hidden+"-->"

def hide_ruby(text):
    """Append hidden hanzi and toneless pinyin to a ruby string,
    to make a note searchable in the 'browse' window.
    """
    t =  no_tone(ruby_top(text))
    t += re.sub(" ", "", no_color(ruby_bottom(text)))
    return hide(text, t)


def no_hidden(text):
    """Remove hidden keyword string"""
    return re.sub("<!--.*?-->", "", text)

    
def accentuate_pinyin(text, force=False):
    u'''Add accents to pinyin. 
    Eg: ni2 becomes ní.
    Eg: ní4 becomes nì. (to make correction easier)
    
    Does nothing if the default transcription is not Pinyin,
    unless force=True.
    Nota : also removes coloring. If you want color, please add it last.
   '''
    def accentuate_pinyin_sub(p):
        pinyin = p.group(1)
        tone = p.group(2)
        if "tone"==pinyin:
            return pinyin+tone
#        for v in accents:            
#            re.sub(v, base_letters[v], pinyin)
        pinyin = no_tone(pinyin)
        for v in u"aeiouüvAEIOUÜV":
            if pinyin.find(v)>-1:
                try:
                    return re.sub(v, vowel_decorations[int(tone)][v.lower()], pinyin, count=1)
                except KeyError, IndexError:
                    pass
        return pinyin
    

    if not 'Pinyin'== chinese_support_config.options['transcription'] and not force:
        return text
    text = no_color(text)
    text = re.sub(r'[vV]', 'ü', text, count=1)
    text = re.sub(u'([a-z]*[aeiouüÜv'+accents+r'][a-z]*)([1-5])', accentuate_pinyin_sub, text, flags=re.I)
    return text

def no_accents(text):
    u'Eg: ní becomes ni2.'
    
    def desaccentuate_pinyin_sub(p):
        return ""+p.group(1)+base_letters[p.group(2)]+p.group(3)+get_tone_number(p.group(2))

    return re.sub(r'([a-z]*)(['+accents+'])([a-z]*)', desaccentuate_pinyin_sub, text, flags=re.I)

def ruby(text, transcription=None, only_one=False, try_dict_first=True):
    u'''Convert hanzi to ruby notation, eg: '你' becomes '你[nǐ]'.
    This can in turn be used with the {{Ruby:fieldname}} card template,
    to generate beautiful ruby-annotated cards.

    If not specified, use the transcription type set in the menubar (eg pinyin).

    if try_dict_first, looks up sequences of characters in the
    selected words dictionary to supply a better transcription.

    If not specified, insert all possible pinyin words for characters not found
    in words dictionary.
    '''
    if transcription == None:
        transcription = chinese_support_config.options['transcription']

    #Replace Chinese typography with its ASCII counterpart
    text = re.sub(u'[［【]', u'[', text)
    text = re.sub(u'[］】]', u']', text)
    #Strip former HTML tone marking and comments
    text = no_color(text)
    text = no_sound(text)
    #Make sure sound tag isn't confused with Hanzi
    text = re.sub(u'([\u4e00-\u9fff])(\[sound:)', r'\1 \2', text)

    def insert_multiple_pinyin_sub(p):
        hanzi=p.group(1)
        transc = translate_module.transcribe_cjklib(hanzi)
        if not transc:
            return p.group()
        transc = transc.split(" ")
        ret = ""
        hanzi = p.group(1)
        while len(hanzi):
            if "Pinyin" == transcription:            
                ret += hanzi[0] + "["+transc.pop(0)+"]"
            elif "Bopomofo" == transcription:
                ret += hanzi[0] + "["
                ret += bopomofo_module.bopomofo(no_accents(transc.pop(0)))+"]"
            hanzi = hanzi[1:]
        return ret+p.group(2)
    
    def insert_pinyin_sub(p):
        return p.group(1)+'['+get_character_transcription(p.group(1), transcription, only_one)+']'+p.group(2)

    text += '%'
    if try_dict_first and transcription in ["Pinyin", "Bopomofo"]:
        text = re.sub(u'([\u4e00-\u9fff]+)([^[])', insert_multiple_pinyin_sub, text)
    text = re.sub(u'([\u4e00-\u9fff])([^[])', insert_pinyin_sub, text)
    text = re.sub(u'([\u4e00-\u9fff])([^[])', insert_pinyin_sub, text)
    text = text[:-1]
    text += sound(text)
    return text

def no_tone(text):
    u'''Removes tone information and coloring.
    Eg: 'ni3' becomes 'ni', 'má' becomes 'ma'
    '''
    text = no_color(text)
    text = no_accents(text)
    def no_tone_marks_sub(p):
        return ""+p.group(1)+re.sub(r'1?[0-9¹²³⁴]', '', p.group(2))+"]"
    if has_ruby(text):
        text = re.sub(u'([\u4e00-\u9fff]\[)([^[]+?)\]', no_tone_marks_sub, text)
    else:
        text = re.sub(r'([a-z]+)1?[0-9¹²³⁴]', r'\1', text)
    return text

def hanzi(text):
    u'''Returns just the anzi from a Ruby notation. 
    Eg: '你[nǐ][You]' becomes '你'.
    '''    
    text = re.sub(u'([\u4e00-\u9fff])(\[[^[]+?\])', r'\1', text)
    text = re.sub(r'\[sound:.[^[]+?\]', '', text)
    text = re.sub(r'([^\u4e00-\u9fff])\[[^[]+?\]\s*$', r'\1', text)
    return text

def transcribe(text, transcription=None, only_one=True, try_dict_first=True):
    u'''
    Converts to specified transcription.
    Eg : 你 becomes nǐ (transcription="Pinyin", only_one=True)

    if try_tict_first is set and transcription is Pinyin or Bopomofo, 
    then first try to lookup word in the selected dictionary. 
    If it fails, or if there were multiple possible transcriptions, then 
    look up each character one by one. 

    For possible transcription choices, please see the Anki drop-down menu.
    Tools->Add-ons->Chinese support->Set transcription

    If no transcription is specified, use the transcription set in the menu.

    In the case of a 多音字 (characters with multiple pronunciations), 
    gives all possible pronunciations, unless only_one is set to False.
    Eg : '了' becomes 'le liǎo' (transcription="Pinyin", only_one=False).
    '''

    def trans_word_sub(p):
        r = translate_module.transcribe_cjklib(p.group(1))
        if r:
            if "Pinyin" == transcription:
                return " " + r + " "
            elif "Bopomofo" == transcription:
                bopo = ""
                for c in no_accents(r).split(" "):
                    bopo += bopomofo_module.bopomofo(c)
                return bopo
        else:
            return p.group()

    def trans_sub(p):
        return " " + get_character_transcription(p.group(1), transcription, only_one) + " "

    if transcription == None:
        transcription = chinese_support_config.options['transcription']
            
    if try_dict_first and transcription in ["Pinyin", "Bopomofo"]:
        text = re.sub(u'\s?([\u4e00-\u9fff]+)\s?', trans_word_sub, text)

    text = re.sub(u'\s?([\u4e00-\u9fff])\s?', trans_sub, text)
    if " " == text[-1:]:
        text=text[:-1]
    if " " == text[:1]:
        text=text[1:]
    return text



def translate(text, from_lang="zh", to_lang=None, max_nb_lines=None):
    u'''Translate to a diferent language. 
    Eg: '你好' becomes 'Hello'
    Only installed dictionaries can be used.

    If the text is made of words taken from the dictionary, than use them directly.
    Otherwise, 

    to_lang possible values : en (English), de (German), fr (French)
    if to_lang is unspecified, the default language will be used.
    '''
    if "zh" != from_lang:
        return "(translation from languages other than Chinese : not available yet.)"
    if None != to_lang:
        return "(specifying translation language: not available yet.)"
    text = translate_module.translate(text)
    if max_nb_lines:
        regex=""
        while max_nb_lines>0:
            regex += ".*?<br/?>"
            max_nb_lines -= 1
        text = re.sub("(^"+regex+").*", r"\1", text, flags=re.I)
    return text


def colorize_fuse(hanzi, pinyin):
    u'''Gives color to a Hanzi phrase based on the tone info from a 
    corresponding Pinyin phrase.

    Eg: "你好" and "ni3 hao3" ->  你好 (both colorized as 3rd tone).
    '''
    pinyin = no_color(pinyin)
    pinyin = re.sub(r"^\s*", "", pinyin)
    pinyin = re.sub(r"\s*$", "", pinyin)
    pinyin = re.split("\s+", pinyin)
    def colorize_fuse_sub(p):
        try:
            return u'<span class="tone{t}">{r}</span>'.format(t=get_tone_number(pinyin.pop(0)), r=p.group())
        except :
            return p.group()
    text = re.sub(u'[\u4e00-\u9fff]', colorize_fuse_sub, hanzi)
    return text

def pinyin(text):
    return transcribe(text, transcription="Pinyin", only_one=False)

def mean_word(text):
    return "(Mean Word generation : not available yet.)"

def sound(text, source=None):
    '''
    Returns sound tag for a given Hanzi string.

    If the sound does not already exist in the media directory, then
    attempt to obtain it from the specified source.
    if the specified source is omitted, use the one selected in the
    tools menu.
    If it fails (eg: no network connexion while trying to retrieve 
    speech from Google TTS), return nothing.

    Does not work with pinyin or other transcriptions.
    '''
    if None==source:
        source = chinese_support_config.options['speech']
    if "Google TTS Mandarin" != source:
        return ""
    text = no_color(no_accents(no_sound(text)))
    if has_ruby(text):
        text = hanzi(text)
    if "" == text:
        return ""
    try:
        return "[sound:"+google_tts.get_word_from_google(text)+"]"
    except:
        return ""


def get_any(fields, dico):
    u'''Get the 1st valid field from a list
    Scans all field names listed as "fields", to find one that exists,
    then returns its value.
    If none exists, returns an empty string.

    Case-insensitive.
    '''
    for f in fields:
        for k, v in dico.iteritems():
            if f.lower()==k.lower():
                return dico[k]
    return ""

def set_all(fields, dico, to):
    u'''Set all existing fields to the same value. 
    (Non-existing fields are ignored)

    Case-insensitive.
    '''
    for f in fields:
        for d, v in dico.iteritems():
            if d.lower()==f.lower():
                dico[d] = to

def has_field(fields, dico):
    u'''
    Check if one of the named fields exists in the field list

    Case-insensitive.
    '''
    for d, v in dico.iteritems():
        for f in fields:
            if f.lower() == d.lower():
                return True
    return False

def no_sound(text):
    u''' 
    Removes the [sound:xxx.mp3] tag that's added by Anki when you record
    sound into a field.  

    If you don't remove it before taking data from one field to another,
    it will likely be duplicated, and the sound will play twice.
    '''
    return re.sub(r'\[sound:.*?]', '', text)

    

# Extra support functions and parameters
##################################################################

vowel_tone_dict = {
    u'ā':1, u'ā':1, u'ɑ̄':1, u'ē':1, u'ī':1, u'ō':1, u'ū':1,
    u'ǖ':1, u'Ā':1, u'Ē':1, u'Ī':1, u'Ō':1, u'Ū':1, u'Ǖ':1,
    u'á':2, u'ɑ́':2, u'é':2, u'í':2, u'ó':2, u'ú':2, u'ǘ':2,
    u'Á':2, u'É':2, u'Í':2, u'Ó':2, u'Ú':2, u'Ǘ':2,
    u'ǎ':3, u'ɑ̌':3, u'ě':3, u'ǐ':3, u'ǒ':3, u'ǔ':3, u'ǚ':3,
    u'Ǎ':3, u'Ě':3, u'Ǐ':3, u'Ǒ':3, u'Ǔ':3, u'Ǚ':3,
    u'à':4, u'ɑ̀':4, u'è':4, u'ì':4, u'ò':4, u'ù':4, u'ǜ':4,
    u'À':4, u'È':4, u'Ì':4, u'Ò':4, u'Ù':4, u'Ǜ':4
    }

vowel_decorations = [
{ },
{ u'a':u'ā', u'e':u'ē', u'i':u'ī', u'o':u'ō', u'u':u'ū', u'ü':u'ǖ', u'v':u'ǖ'},
{ u'a':u'á', u'e':u'é', u'i':u'í', u'o':u'ó', u'u':u'ú', u'ü':u'ǘ', u'v':u'ǘ'},
{ u'a':u'ǎ', u'e':u'ě', u'i':u'ǐ', u'o':u'ǒ', u'u':u'ǔ', u'ü':u'ǚ', u'v':u'ǚ'},
{ u'a':u'à', u'e':u'è', u'i':u'ì', u'o':u'ò', u'u':u'ù', u'ü':u'ǜ', u'v':u'ǜ'},
{ u'a':u'a', u'e':u'e', u'i':u'i', u'o':u'o', u'u':u'u', u'ü':u'ü', u'v':u'ü'},
]

base_letters = { 
u'ā':u'a', u'ē':u'e', u'ī':u'i', u'ō':u'o', u'ū':u'u', u'ǖ':u'ü',  
u'á':u'a', u'é':u'e', u'í':u'i', u'ó':u'o', u'ú':u'u', u'ǘ':u'ü',  
u'ǎ':u'a', u'ě':u'e', u'ǐ':u'i', u'ǒ':u'o', u'ǔ':u'u', u'ǚ':u'ü',  
u'à':u'a', u'è':u'e', u'ì':u'i', u'ò':u'o', u'ù':u'u', u'ǜ':u'ü',  
u'a':u'a', u'e':u'e', u'i':u'i', u'o':u'o', u'u':u'u', u'ü':u'ü', 
}

accents = u'ɑ̄āĀáɑ́ǎɑ̌ÁǍàɑ̀ÀēĒéÉěĚèÈīĪíÍǐǏìÌōŌóÓǒǑòÒūŪúÚǔǓùÙǖǕǘǗǚǙǜǛ'

characterLookup = characterlookup.CharacterLookup('C')
#One of TCJKV. I don't know what difference it makes

bopomofo_notes = {
 u"ˊ":"2", u"ˇ":"3",u"ˋ":"4", u"˙":"5"}

def extract_sound_tags(text):
    sound_tags = re.findall(r"\[sound:.*?\]", text)
    if [] == sound_tags:
        sound_tags=""
    else:
        sound_tags = reduce(lambda a,b:a+b, sound_tags)
    nosound = re.sub(r"\[sound:.*?\]", r"", text)
    return nosound, sound_tags


def get_tone_number(pinyin):
    if re.match(r".+1[0-9]$", pinyin):
        return pinyin[-2:]
    elif re.match(r".+[0-9]$", pinyin):
        return pinyin[-1:]
    elif re.match(u".+[¹²³⁴]$", pinyin):
        return str(u" ¹²³⁴".index(pinyin[-1:]))
    elif re.match(u"[\u3100-\u312F]", pinyin):#Bopomofo
        if re.match(u"[ˊˇˋ˙]", pinyin[-1:]):
            return str(u"  ˊˇˋ˙".index(pinyin[-1:]))
        else:
            return "1"
    else:
        for c in pinyin:
            try:
                return str(vowel_tone_dict[c])
            except KeyError:
                continue
        return "5"


def has_ruby(text):
    return re.match(u"[\u4e00-\u9fff]\[.+\]", text)

def has_hanzi(text):
    return re.match(u"[\u4e00-\u9fff]", text)

def get_character_transcription(hanzi, transcription=None, only_one=False):
    if transcription == None:
        transcription = chinese_support_config.options['transcription']
    if "Bopomofo" == transcription:
        transcription="Pinyin"
        bopomofo=True
    else:
        bopomofo=False

    def concat(a, b):
        return a+' '+b
    transcriptions = characterLookup.getReadingForCharacter(hanzi, transcription)
    if 0 == len(transcriptions):
        text = ""
    elif only_one:
        text = transcriptions[0]
    else:
        text = reduce(concat, transcriptions)
    if bopomofo:
        text = bopomofo_module.bopomofo(no_accents(text))
    return text

