# -*- coding: utf-8 -*-
#
# Copyright © 2012 Thomas TEMPÉ, <thomas.tempe@alysse.org>
# 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from aqt import mw
import re

from config import chinese_support_config
import bopomofo as bopomofo_module
import google_tts
import baidu_tts
from microsofttranslator import Translator as MSTranslator
import dictdb

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
        pinyin = p.group()
        if pinyin[0] in '&<"/':
            return pinyin
        else:
            return u'<span class="tone{t}">{r}</span>'.format(t=get_tone_number(p.group(1)), r=pinyin)


    if has_ruby(text): #Treat like ruby
        if ruby_whole:
            def colorize_ruby_sub(p):
                return u'<span class="tone{t}">{r}</span>'.format(t=get_tone_number(p.group(2)), r=p.group())

            text = re.sub(u'([\u3400-\u9fff]\[\s*)([a-zü'+accents+u']+1?[0-9¹²³⁴]?)(.*?\])', colorize_ruby_sub, text, flags=re.I)    
        else:
            text = re.sub(u'([a-zü'+accents+u']+1?[0-9¹²³⁴]?)', colorize_pinyin_sub, text, flags=re.I)
    elif has_hanzi(text):
        text = re.sub(u'([\u3400-\u9fff])', colorize_hanzi_sub, text)
    else:
        text = re.sub(u'([&<"/]?[a-zü'+accents+u']+1?[0-9¹²³⁴]?)', colorize_pinyin_sub, text, flags=re.I)
    text = text+sound_tags
    return text

def ruby_top(txt):
    "Extract the top (pronunciation) part of a ruby string."
    r = r' ?([^ >]+?)\[(.+?)\]'
    return re.sub(r, r'\2 ', no_sound(txt))

def ruby_bottom(txt):
    "Extract the bottom part of a ruby string."
    r = r' ?([^ >]+?)\[(.+?)\]'
    text = re.sub(r, r'\1 ', no_sound(txt))
    return text

def no_color(text):
    "Remove tone color info and other HTML pollutions"
    if text == None:
        return ""
    text = text.replace(r'&nbsp;', '')
    text = no_hidden(text)
    #remove color info
    text = re.sub(r'<span class="tone1?[0-9]">(.*?)</span>', r'\1', text)
    #remove black font tag sometimes added by Anki
    text = re.sub(r'<font color="#000000">(.*?)</font>', r'\1', text)
    return text

def hide(text, hidden):
    """Add hidden keyword to string (typically Hanzi and toneless pinyin),
    to make a note searchable in the 'browse' window
    """
    if len(text) == 0 or text == "<br />":
        return ""
    hidden = no_color(hidden)
    hidden = hidden.replace("<.*?>", "")
    hidden = hidden.replace(r"[<!->]", "")
    return text + "<!--"+hidden+"-->"

def hide_ruby(text):
    """Append hidden hanzi and toneless pinyin to a ruby string,
    to make a note searchable in the 'browse' window.
    """
    t =  no_tone(ruby_top(text))
    t += no_color(ruby_bottom(text)).replace(" ", "")
    return hide(text, t)


def silhouette(hanzi):
    """Replaces each Chinese character by a blank space.

    Eg: 以A为B -> _A_B
    Eg: 哈密瓜 -> _ _ _
    """
    def insert_spaces(p):
        r = ""
        for i in p.group(0):
            r += i + " "
        return r[:-1]

    hanzi = re.sub(u"[\u3400-\u9fff]+", insert_spaces, hanzi)
    txt = re.sub(u"[\u3400-\u9fff]", "_", hanzi)
    return txt


def no_hidden(text):
    """Remove hidden keyword string"""
    return re.sub(r"<!--.*?-->", "", text)
    
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
    text = re.sub(u'([a-z]*[aeiouüÜv'+accents+u'][a-zü]*)([1-5])', accentuate_pinyin_sub, text, flags=re.I)
    return text

def no_accents(text):
    u'Eg: ní becomes ni2.'
    
    def desaccentuate_pinyin_sub(p):
        return ""+p.group(1)+base_letters[p.group(2).lower()]+p.group(3)+get_tone_number(p.group(2).lower())

    return re.sub(u'([a-zü]*)(['+accents+u'])([a-zü]*)', desaccentuate_pinyin_sub, text, flags=re.I)

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
    text = re.sub(u'([\u3400-\u9fff])(\[sound:)', r'\1 \2', text)

    def insert_multiple_pinyin_sub(p):
        hanzi=p.group(1)
        transc = db.get_pinyin(hanzi)
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
        text = re.sub(u'([\u3400-\u9fff]+)([^[])', insert_multiple_pinyin_sub, text)
    text = re.sub(u'([\u3400-\u9fff])([^[])', insert_pinyin_sub, text)
    text = re.sub(u'([\u3400-\u9fff])([^[])', insert_pinyin_sub, text)
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
        text = re.sub(u'([\u3400-\u9fff]\[)([^[]+?)\]', no_tone_marks_sub, text)
    else:
        text = re.sub(u'([a-zü]+)1?[0-9¹²³⁴]', r'\1', text)
    return text

def hanzi(text):
    u'''Returns just the anzi from a Ruby notation. 
    Eg: '你[nǐ][You]' becomes '你'.
    '''
    text = re.sub(u'([\u3400-\u9fff])(\[[^[]+?\])', r'\1', text)
    text = re.sub(r'\[sound:.[^[]+?\]', '', text)
    text = re.sub(r'([^\u3400-\u9fff])\[[^[]+?\]\s*$', r'\1', text)
    return text

def transcribe(text, transcription=None, only_one=True):
    u'''
    Converts to specified transcription.
    Eg : 你 becomes nǐ (transcription="Pinyin", only_one=True)

    Pinyin, Taiwan Pinyin and Bopomofo: lookup in local words dictionaries
    first, and use characters dictionary as a backup.

    If no transcription is specified, use the transcription set in the menu.
    '''
    text = cleanup(text)
    if text == "":
        return ""
    if None == transcription:
        transcription = chinese_support_config.options["transcription"]
    if "Pinyin" == transcription:
        r = db.get_pinyin(text)
    elif "Pinyin (Taiwan)" == transcription:
        r = db.get_pinyin(text, taiwan=True)
    elif "Cantonese" == transcription:
        r = db.get_cantonese(text, only_one)
    elif "Bopomofo" == transcription:
        r = db.get_pinyin(text, taiwan=True)
        r = bopomofo_module.bopomofo(no_accents(r))
    else:
        r = ""
    return r

def get_alt(text):
    """Returns alternate spelling of Chinese expression"""

def translate_local(text, lang):
    """Translate using local dictionary.

    lang is one of "en", "fr", "de", "es"
    """
    defs =  db.get_definitions(text, lang)
    if 0 == len(defs):
        return ""
    def are_there_multiple_pinyins(defs):
        (prev_p, a, b, c)= defs[0]
        for (pinyin, definition, cl, alt) in defs:
            if pinyin<>prev_p:
                return True
        return False

    res = ""
    if are_there_multiple_pinyins(defs):
        for (pinyin, definition, cl, alt) in defs:
            res += u"❖ %s[%s] %s\n" % (text, pinyin, definition)
    else:
        for (pinyin, definition, cl, alt) in defs:
            res += " \t"+definition+"\n"        

    res = res.replace("\n", "\n<br>")
    res = local_dict_colorize(res)
    return res

def translate(text, from_lang="zh", to_lang=None, progress_bar=True):
    u'''Translate to a different language. 
    Eg: '你好' becomes 'Hello'
    Only installed dictionaries can be used.

    to_lang possible values : "local_en", "local_de", "local_fr"
    or a 2-letter ISO language code for MS Translate
    
    if to_lang is unspecified, the default language will be used.
    if progress_bar is True, then will display a progress bar.
    '''
    global MS_translator_object
    text = cleanup(text)
    if "" == text:
        return ""
    if None == to_lang:
        to_lang = chinese_support_config.options["dictionary"]
        if "None" == to_lang:
            return ""
    if to_lang.startswith("local_"): #Local dict
        return translate_local(text, to_lang[-2:])
    else:  #Ms translate
        ret = ""
        if progress_bar:
            mw.progress.start(label="MS Translator lookup", immediate=True)
        if None == MS_translator_object:
            MS_translator_object = MSTranslator("chinese-support-add-on", "Mh+X5YY17LZZ8rO9hzJXYD3I02V3E+ltItF15ep7qG8=")
        try:
            ret = MS_translator_object.translate(text, to_lang)
        except:
            pass
        
        if "ArgumentException:" == ret[:18]:
            #Token has probably expired
            ret=""
        if progress_bar:
            mw.progress.finish()
        return ret

def cleanup(txt):
    if not txt:
        return ""
    txt = re.sub(r"<.*?>", "", txt)
    txt = txt.replace("&nbsp;", " ")
    txt = re.sub(r"^\s*", "", txt)
    txt = re.sub(r"\s*$", "", txt)
#    txt = re.sub(r"[\s+]", " ", txt)
    return txt


def colorize_fuse(hanzi, pinyin, ruby=False):
    u'''Gives color to a Hanzi phrase based on the tone info from a 
    corresponding Pinyin phrase.
    If ruby = True, then annotate with pinyin on top of each character

    Eg: "你好" and "ni3 hao3" ->  你好 (both colorized as 3rd tone).
    '''
    pinyin = cleanup(no_color(pinyin))+" "*len(hanzi)
    hanzi  = cleanup(hanzi)
    text = ""
#    print hanzi, "\t", pinyin
    for h in hanzi:
        if len(pinyin)<5:
            pinyin = pinyin+"     "
        if has_hanzi(h):
            [p, pinyin] = pinyin.split(" ", 1)
#            print "C1\t", h, "\t", p
            if ruby:
                text +=  u'<span class="tone{t}"><ruby>{h}<rt>{p}</rt></span>'.format(t=get_tone_number(p), h=h, p=p)
            else:
                text +=  u'<span class="tone{t}">{h}</span>'.format(t=get_tone_number(p), h=h)
        elif " "==h and " "!=pinyin[0]:
            text += " "
#            print "C2\t_\t(none)"
        else:
#            print "C3\t", h, "\t", pinyin[0]
            text += pinyin[0]
            pinyin = pinyin[1:]
            if " " == pinyin[0]:
                pinyin = pinyin[1:]
    return text

def pinyin(text):
    return transcribe(text, transcription="Pinyin")

def get_mean_word(text):
    if text == "":
        return ""
    cl =  db.get_classifiers(text)
    if len(cl):
        return local_dict_colorize(", ".join(cl))
    else:
        return ""

def get_alternate_spellings(text):
    if text == "":
        return ""
    alt =  db.get_alt_spellings(text)
    if len(alt):
        return local_dict_colorize(", ".join(alt))
    else:
        return ""

def sound(text, source=None):
    '''
    Returns sound tag for a given Hanzi string.

    If the sound does not already exist in the media directory, then
    attempt to obtain it from the specified source.
    if the specified source is omitted, use the one selected in the
    tools menu.
    If it fails (eg: no network connexion while trying to retrieve 
    speech from Google TTS), return empty string.

    Does not work with pinyin or other transcriptions.
    '''
    text = cleanup(text)
    if None==source:
        source = chinese_support_config.options['speech']

    text = no_color(no_accents(no_sound(text)))
    text = re.sub("<.*?>", "", text)
    if has_ruby(text):
        text = hanzi(text)
    if "" == text:
        return ""

    if "Google TTS Mandarin" == source:
        try:
            return "[sound:"+google_tts.get_word_from_google(text)+"]"
        except:
            return ""
    elif "Baidu Translate" == source:
        try:
            return "[sound:"+baidu_tts.get_word_from_baidu(text)+"]"
        except:
            return ""        
    else:
        return ""

def check_for_sound(text):
    '''
    Returns True if the soundfile arleady exists in the user's resources directory.
    '''
    text = cleanup(text)
    text = no_color(no_accents(no_sound(text)))
    text = re.sub("<.*?>", "", text)
    if has_ruby(text):
        text = hanzi(text)
    if "" == text:
        return False
    if google_tts.check_resources(text):
        return True
    return False


def get_any(fields, dico):
    u'''Get the 1st valid field from a list
    Scans all field names listed as "fields", to find one that exists,
    then returns its value.
    If none exists, returns an empty string.

    Case-insensitive.
    '''
    for f in fields:
        for k, v in dico.iteritems():
            try:
                if unicode(f.lower()) == unicode(k.lower()):
                    return dico[k]
            except:
                pass
    return ""

def set_all(fields, dico, to):
    u'''Set all existing fields to the same value. 
    (Non-existing fields are ignored)

    Case-insensitive.
    '''
    for f in fields:
        for d, v in dico.iteritems():
            try:
                if unicode(d.lower()) == unicode(f.lower()):
                    dico[d] = to
            except:
                pass

def has_field(fields, dico):
    u'''
    Check if one of the named fields exists in the field list

    Case-insensitive.
    '''
    for d, v in dico.iteritems():
        for f in fields:
            try:
                if unicode(f.lower()) == unicode(d.lower()):
                    return True
            except:
                pass
    return False

def no_sound(text):
    u''' 
    Removes the [sound:xxx.mp3] tag that's added by Anki when you record
    sound into a field.  

    If you don't remove it before taking data from one field to another,
    it will likely be duplicated, and the sound will play twice.
    '''
    return re.sub(r'\[sound:.*?]', '', text)

def separate_pinyin(text, force=False):
    u"""
    Separate pinyin syllables with whitespace.
    Eg: "Yīlù píng'ān" becomes "Yī lù píng ān"

    Does nothing if the default transcription is not pinyin, 
    unless Force=True
    Useful for people pasting Pinyin from Google Translate.
    """
    if chinese_support_config.options['transcription'] \
            not in ['Pinyin', 'Pinyin (Taiwan)'] and not force:
        return text
    def clean(t):
        'remove leading apostrophe'
        if "'" == t[0]:
            return t[1:]
        return t
    def separate_pinyin_sub(p):
        return clean(p.group("one"))+" "+clean(p.group("two"))
    text =  pinyin_two_re.sub(separate_pinyin_sub, text)
    text =  pinyin_two_re.sub(separate_pinyin_sub, text)
    return text
    
def simplify(text):
    u'''Converts to simplified variants (if they exist)
    '''
    r = db.get_simplified(text)
    if r != text:
        return r
    else:
        return ""

def traditional(text):
    u'''Converts to traditional variants (if they exist)
    '''
    r = db.get_traditional(text)
    if r != text:
        return r
    else:
        return ""


# Extra support functions and parameters
##################################################################

MS_translator_object = None

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


def pinyin_re_sub():
    inits = u"zh|sh|ch|[bpmfdtnlgkhjqxrzscwy]"
    finals = u"i[ōóǒòo]ng|[ūúǔùu]ng|[āáǎàa]ng|[ēéěèe]ng|i[āɑ̄áɑ́ɑ́ǎɑ̌àɑ̀aāáǎàa]ng|[īíǐìi]ng|i[āáǎàa]n|u[āáǎàa]n|[ōóǒòo]ng|[ēéěèe]r|i[āáǎàa]|i[ēéěèe]|i[āáǎàa]o|i[ūúǔùu]|[īíǐìi]n|u[āáǎàa]|u[ōóǒòo]|u[āáǎàa]i|u[īíǐìi]|[ūúǔùu]n|u[ēéěèe]|ü[ēéěèe]|v[ēéěèe]|i[ōóǒòo]|[āáǎàa]i|[ēéěèe]i|[āáǎàa]o|[ōóǒòo]u|[āáǎàa]n|[ēéěèe]n|[āáǎàa]|[ēéěèe]|[ōóǒòo]|[īíǐìi]|[ūúǔùu]|[ǖǘǚǜüv]"
    standalones = u"'[āáǎàa]ng|'[ēéěèe]ng|'[ēéěèe]r|'[āáǎàa]i|'[ēéěèe]i|'[āáǎàa]o|'[ōóǒòo]u|'[āáǎàa]n|'[ēéěèe]n|'[āáǎàa]|'[ēéěèe]|'[ōóǒòo]"
    return "(("+inits+")("+finals+")[1-5]?|("+standalones+")[1-5]?)"

pinyin_re = pinyin_re_sub()
pinyin_two_re = re.compile("(?P<one>"+pinyin_re+")(?P<two>"+pinyin_re+")", flags=re.I)

db = dictdb.DictDB()

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
    return re.search(u"[\u3400-\u9fff]\[.+\]", text)

def has_hanzi(text):
    return re.search(u"[\u3400-\u9fff]", text)


def get_character_transcription(hanzi, transcription=None):
    if transcription == None:
        transcription = chinese_support_config.options['transcription']

    if "Pinyin" == transcription:
        text = db.get_pinyin(hanzi)
    elif "Pinyin (Taiwan)" == transcription:
        text = db.get_pinyin(hanzi, taiwan=True)
    elif "Cantonese" == transcription:
        text = db.get_cantonese(hanzi)
    elif "Bopomofo" == transcription:
        text = db.get_pinyin(hanzi, taiwan=True)
        text = bopomofo_module.bopomofo(no_accents(text))
    else:
        text = ""
    return text

def add_diaeresis(text):
    try:
        return re.sub(u"v", u"ü", text)
    except:
        return ""


def local_dict_colorize(txt, ruby=True):
    """
    Colorize text in the form :
    "Hello is written 你好[ni3 hao]"
    (as used in the local dictionaries)
    """
    def _sub(p):
        c = ""
        hanzi = p.group(1)
        pinyin = p.group(2)
        pinyin = accentuate_pinyin(pinyin)
 
        if ruby:
            if 1 == hanzi.count("|"):
                hanzi = hanzi.split("|")
                c += colorize_fuse(hanzi[0], pinyin, True)
                c += "|"
                c += colorize_fuse(hanzi[1], pinyin, True)
            else:
                c += colorize_fuse(hanzi, pinyin, True)
        else:
            if 1 == hanzi.count("|"):
            #Hanzi has 2 variants (traditional and simplified)
                hanzi = hanzi.split("|")
                c += colorize_fuse(hanzi[0], pinyin, False)
                c += "|"
                c += colorize_fuse(hanzi[1], pinyin, False)
            else:
                c += colorize_fuse(hanzi, pinyin, False)
            c += "[" + colorize(pinyin) + "]"
        return c

    txt = re.sub(u"([\u3400-\u9fff|]+)\\[(.*?)\\]", _sub, txt)
    return txt
    
