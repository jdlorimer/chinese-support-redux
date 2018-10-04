# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from functools import reduce
import re

from aqt import mw

from . import baidu_tts
from . import bopomofo as bopomofo_module
from . import dictdb
from . import google_tts
from .util import *
from .config import chinese_support_config


def colorize(text, ruby_whole=False):
    '''Add tone color info.
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
        return '<span class="tone{t}">{r}</span>'.format(t=get_tone_number(transcribe(p.group(1), only_one=True)), r=p.group())

    def colorize_pinyin_sub(p):
        pinyin = p.group()
        if pinyin[0] in '&<"/':
            return pinyin
        else:
            return '<span class="tone{t}">{r}</span>'.format(t=get_tone_number(p.group(1)), r=pinyin)


    if has_ruby(text): #Treat like ruby
        if ruby_whole:
            def colorize_ruby_sub(p):
                return '<span class="tone{t}">{r}</span>'.format(t=get_tone_number(p.group(2)), r=p.group())

            text = re.sub('([\u3400-\u9fff]\[\s*)([a-zü'+accents+']+1?[0-9¹²³⁴]?)(.*?\])', colorize_ruby_sub, text, flags=re.I)
        else:
            text = re.sub('([a-zü'+accents+']+1?[0-9¹²³⁴]?)', colorize_pinyin_sub, text, flags=re.I)
    elif has_hanzi(text):
        text = re.sub('([\u3400-\u9fff])', colorize_hanzi_sub, text)
    else:
        text = re.sub('([&<"/]?[a-zü\u3100-\u312F'+accents+']+1?[0-9¹²³⁴ˊˇˋ˙]?)', colorize_pinyin_sub, text, flags=re.I)
    text = text+sound_tags
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
    #remove Anki1 Pinyin Toolkit coloring
    text = re.sub(r'<span style=.*?>(.*?)</span>', r'\1', text)
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

    hanzi = re.sub("[\u3400-\u9fff]+", insert_spaces, hanzi)
    txt = re.sub("[\u3400-\u9fff]", "_", hanzi)
    return txt


def accentuate_pinyin(text, force=False):
    '''Add accents to pinyin.
    Eg: ni2 becomes ní.
    Eg: ní4 becomes nì. (to make correction easier)

    Does nothing if the default transcription is not Pinyin or Pinyin (Taiwan),
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
        for v in "aeouüviAEOUÜVI":
            if pinyin.find(v)>-1:
                try:
                    return re.sub(v, vowel_decorations[int(tone)][v.lower()], pinyin, count=1)
                except (KeyError, IndexError):
                    pass
        return pinyin

    if chinese_support_config.options['transcription'] \
            not in ['Pinyin', 'Pinyin (Taiwan)'] and not force:
        return text
    text = no_color(text)
    text = re.sub('([a-z]*[aeiouüÜv'+accents+'][a-zü]*)([1-5])', accentuate_pinyin_sub, text, flags=re.I)
    return text

def no_accents(text):
    'Eg: ní becomes ni2.'

    def desaccentuate_pinyin_sub(p):
        return ""+p.group(1)+base_letters[p.group(2).lower()]+p.group(3)+get_tone_number(p.group(2).lower())

    #Remove +u'aeiouüvAEIOUÜV' if you want 5th tone to be ignored
    return re.sub('([a-zü]*)(['+'aeiouüvAEIOUÜV'+accents+'])([a-zü]*)', desaccentuate_pinyin_sub, text, flags=re.I)

def ruby(text, transcription=None, only_one=False, try_dict_first=True):
    '''Convert hanzi to ruby notation, eg: '你' becomes '你[nǐ]'.
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
    text = re.sub('[［【]', '[', text)
    text = re.sub('[］】]', ']', text)
    #Strip former HTML tone marking and comments
    text = no_color(text)
    text = no_sound(text)
    #Make sure sound tag isn't confused with Hanzi
    text = re.sub('([\u3400-\u9fff])(\[sound:)', r'\1 \2', text)

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
        text = re.sub('([\u3400-\u9fff]+)([^[])', insert_multiple_pinyin_sub, text)
    text = re.sub('([\u3400-\u9fff])([^[])', insert_pinyin_sub, text)
    text = re.sub('([\u3400-\u9fff])([^[])', insert_pinyin_sub, text)
    text = text[:-1]
    text += sound(text)
    return text

def no_tone(text):
    '''Removes tone information and coloring.
    Eg: 'ni3' becomes 'ni', 'má' becomes 'ma'
    '''
    text = no_color(text)
    text = no_accents(text)
    def no_tone_marks_sub(p):
        return ""+p.group(1)+re.sub(r'1?[0-9¹²³⁴]', '', p.group(2))+"]"
    if has_ruby(text):
        text = re.sub('([\u3400-\u9fff]\[)([^[]+?)\]', no_tone_marks_sub, text)
    else:
        text = re.sub('([a-zü]+)1?[0-9¹²³⁴]', r'\1', text)
    return text

def hanzi(text):
    '''Returns just the anzi from a Ruby notation.
    Eg: '你[nǐ][You]' becomes '你'.
    '''
    text = re.sub('([\u3400-\u9fff])(\[[^[]+?\])', r'\1', text)
    text = re.sub(r'\[sound:.[^[]+?\]', '', text)
    text = re.sub(r'([^\u3400-\u9fff])\[[^[]+?\]\s*$', r'\1', text)
    return text

def transcribe(text, transcription=None, only_one=True):
    '''
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
        r = db.get_pinyin(text, taiwan=False)
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

def pinyin_to_bopomofo(pinyin):
    '''
    Converts Pinyin to Bopomofo.
    '''
    return bopomofo_module.bopomofo(no_accents(cleanup(pinyin)))

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
            if pinyin != prev_p:
                return True
        return False

    res = ""
    if are_there_multiple_pinyins(defs):
        for (pinyin, definition, cl, alt) in defs:
            res += "❖ %s[%s] %s\n" % (text, pinyin, definition)
    else:
        for (pinyin, definition, cl, alt) in defs:
            res += " \t"+definition+"\n"

    res = res.replace("\n", "\n<br>")
    res = local_dict_colorize(res)
    return res


def translate(text, from_lang="zh", to_lang=None, progress_bar=True):
    '''Translate to a different language.
    Eg: '你好' becomes 'Hello'
    Only installed dictionaries can be used.

    to_lang possible values : "local_en", "local_de", "local_fr"

    if to_lang is unspecified, the default language will be used.
    if progress_bar is True, then will display a progress bar.
    '''
    text = cleanup(text)
    if "" == text:
        return ""
    if None == to_lang:
        to_lang = chinese_support_config.options["dictionary"]
        if "None" == to_lang:
            return ""
    if to_lang.startswith("local_"): #Local dict
        return translate_local(text, to_lang[-2:])


def cleanup(txt):
    '''Remove all HTML, tags, and others.'''
    if not txt:
        return ""
    txt = re.sub(r"<.*?>", "", txt, flags=re.S)
    txt = txt.replace("&nbsp;", " ")
    txt = re.sub(r"^\s*", "", txt)
    txt = re.sub(r"\s*$", "", txt)
#    txt = re.sub(r"[\s+]", " ", txt)
    txt = re.sub(r"\{\{c[0-9]+::(.*?)(::.*?)?\}\}", r"\1", txt)
    return txt


def colorize_fuse(hanzi, pinyin, ruby=False):
    '''Gives color to a Hanzi phrase based on the tone info from a
    corresponding Pinyin phrase.
    If ruby = True, then annotate with pinyin on top of each character

    Eg: "你好" and "ni3 hao3" ->  你好 (both colorized as 3rd tone).
    '''
    pinyin = cleanup(no_color(pinyin))+" "*len(hanzi)
    hanzi  = cleanup(hanzi)
    text = ""
    for h in hanzi:
        if len(pinyin)<5:
            pinyin = pinyin+"     "
        if has_hanzi(h):
            [p, pinyin] = pinyin.split(" ", 1)
            if ruby:
                text +=  '<span class="tone{t}"><ruby>{h}<rt>{p}</rt></span>'.format(t=get_tone_number(p), h=h, p=p)
            else:
                text +=  '<span class="tone{t}">{h}</span>'.format(t=get_tone_number(p), h=h)
        elif " "==h and " "!=pinyin[0]:
            text += " "
        else:
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
    if len(list(cl)):
        return local_dict_colorize(", ".join(cl))
    else:
        return ""

def get_alternate_spellings(text):
    if text == "":
        return ""
    alt =  db.get_alt_spellings(text)
    if len(list(alt)):
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

    Source is either the TTS speech engine name.
    If empty, taking the one from the menu.
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
            return "[sound:"+google_tts.get_word_from_google(text, 'zh')+"]"
        except:
            return ""
    elif "Baidu Translate" == source:
        try:
            return "[sound:"+baidu_tts.get_word_from_baidu(text, 'zh')+"]"
        except:
            return ""
    elif "Google TTS Cantonese" == source:
        try:
            return "[sound:"+google_tts.get_word_from_google(text, 'zh-yue')+"]"
        except:
            return ""
    else:
        return ""



def get_any(fields, dico):
    '''Get the 1st valid field from a list
    Scans all field names listed as "fields", to find one that exists,
    then returns its value.
    If none exists, returns an empty string.

    Case-insensitive.
    '''
    for f in fields:
        for k, v in dico.items():
            try:
                if str(f.lower()) == str(k.lower()):
                    return dico[k]
            except:
                pass
    return ""


def setAll(fields, note, to):
    fields = [f.lower() for f in fields]

    for f in note.keys():
        if f.lower() in fields:
            note[f] = to


def has_field(fields, dico):
    '''
    Check if one of the named fields exists in the field list

    Case-insensitive.
    '''
    for d, v in dico.items():
        for f in fields:
            try:
                if str(f.lower()) == str(d.lower()):
                    return True
            except:
                pass
    return False


def separate_pinyin(text, force=False, cantonese=False):
    """
    Separate pinyin syllables with whitespace.
    Eg: "Yīlù píng'ān" becomes "Yī lù píng ān"

    Does nothing if the default transcription is not Pinyin or Pinyin (Taiwan),
    unless force="Pinyin" or force="Pinyin (Taiwan)" or force=True
    Cantonese sets whether or not the text being separated is cantonese (if force=True).
    Useful for people pasting Pinyin from Google Translate.
    """

    if (chinese_support_config.options['transcription'] \
            in ['Pinyin', 'Pinyin (Taiwan)'] and not force) or (force and not cantonese):
        def clean(t):
            'remove leading apostrophe'
            if "'" == t[0]:
                return t[1:]
            return t
        def separate_pinyin_sub(p):
            return clean(p.group("one"))+" "+clean(p.group("two"))
        text =  pinyin_two_re.sub(separate_pinyin_sub, text)
        return text
    elif (chinese_support_config.options['transcription'] \
            in ['Cantonese'] and not force) or (force and cantonese):
        def clean(t):
            'remove leading apostrophe'
            if "'" == t[0]:
                return t[1:]
            return t
        def separate_jyutping_sub(p):
            return clean(p.group("one"))+" "+clean(p.group("two"))
        text =  jyutping_two_re.sub(separate_jyutping_sub, text)
        text =  jyutping_two_re.sub(separate_jyutping_sub, text)
        return text
    else:
        return text

def simplify(text):
    '''Converts to simplified variants
    '''
    r = db.get_simplified(text)
    return r

def traditional(text):
    '''Converts to traditional variants
    '''
    r = db.get_traditional(text)
    return r


# Extra support functions and parameters
##################################################################

vowel_tone_dict = {
    'ā':1, 'ā':1, 'ɑ̄':1, 'ē':1, 'ī':1, 'ō':1, 'ū':1,
    'ǖ':1, 'Ā':1, 'Ē':1, 'Ī':1, 'Ō':1, 'Ū':1, 'Ǖ':1,
    'á':2, 'ɑ́':2, 'é':2, 'í':2, 'ó':2, 'ú':2, 'ǘ':2,
    'Á':2, 'É':2, 'Í':2, 'Ó':2, 'Ú':2, 'Ǘ':2,
    'ǎ':3, 'ɑ̌':3, 'ě':3, 'ǐ':3, 'ǒ':3, 'ǔ':3, 'ǚ':3,
    'Ǎ':3, 'Ě':3, 'Ǐ':3, 'Ǒ':3, 'Ǔ':3, 'Ǚ':3,
    'à':4, 'ɑ̀':4, 'è':4, 'ì':4, 'ò':4, 'ù':4, 'ǜ':4,
    'À':4, 'È':4, 'Ì':4, 'Ò':4, 'Ù':4, 'Ǜ':4
    }

vowel_decorations = [
{ },
{ 'a':'ā', 'e':'ē', 'i':'ī', 'o':'ō', 'u':'ū', 'ü':'ǖ', 'v':'ǖ'},
{ 'a':'á', 'e':'é', 'i':'í', 'o':'ó', 'u':'ú', 'ü':'ǘ', 'v':'ǘ'},
{ 'a':'ǎ', 'e':'ě', 'i':'ǐ', 'o':'ǒ', 'u':'ǔ', 'ü':'ǚ', 'v':'ǚ'},
{ 'a':'à', 'e':'è', 'i':'ì', 'o':'ò', 'u':'ù', 'ü':'ǜ', 'v':'ǜ'},
{ 'a':'a', 'e':'e', 'i':'i', 'o':'o', 'u':'u', 'ü':'ü', 'v':'ü'},
]

base_letters = {
'ā':'a', 'ē':'e', 'ī':'i', 'ō':'o', 'ū':'u', 'ǖ':'ü',
'á':'a', 'é':'e', 'í':'i', 'ó':'o', 'ú':'u', 'ǘ':'ü',
'ǎ':'a', 'ě':'e', 'ǐ':'i', 'ǒ':'o', 'ǔ':'u', 'ǚ':'ü',
'à':'a', 'è':'e', 'ì':'i', 'ò':'o', 'ù':'u', 'ǜ':'ü',
'a':'a', 'e':'e', 'i':'i', 'o':'o', 'u':'u', 'ü':'ü', 'v':'v'
}

accents = 'ɑ̄āĀáɑ́ǎɑ̌ÁǍàɑ̀ÀēĒéÉěĚèÈīĪíÍǐǏìÌōŌóÓǒǑòÒūŪúÚǔǓùÙǖǕǘǗǚǙǜǛ'


def pinyin_re_sub():
    inits = "zh|sh|ch|[bpmfdtnlgkhjqxrzscwy]"
    finals = "i[ōóǒòo]ng|[ūúǔùu]ng|[āáǎàa]ng|[ēéěèe]ng|i[āɑ̄áɑ́ɑ́ǎɑ̌àɑ̀aāáǎàa]ng|[īíǐìi]ng|i[āáǎàa]n|u[āáǎàa]n|[ōóǒòo]ng|[ēéěèe]r|i[āáǎàa]|i[ēéěèe]|i[āáǎàa]o|i[ūúǔùu]|[īíǐìi]n|u[āáǎàa]|u[ōóǒòo]|u[āáǎàa]i|u[īíǐìi]|[ūúǔùu]n|u[ēéěèe]|ü[ēéěèe]|v[ēéěèe]|i[ōóǒòo]|[āáǎàa]i|[ēéěèe]i|[āáǎàa]o|[ōóǒòo]u|[āáǎàa]n|[ēéěèe]n|[āáǎàa]|[ēéěèe]|[ōóǒòo]|[īíǐìi]|[ūúǔùu]|[ǖǘǚǜüv]"
    standalones = "'[āáǎàa]ng|'[ēéěèe]ng|'[ēéěèe]r|'[āáǎàa]i|'[ēéěèe]i|'[āáǎàa]o|'[ōóǒòo]u|'[āáǎàa]n|'[ēéěèe]n|'[āáǎàa]|'[ēéěèe]|'[ōóǒòo]"
    return "(("+inits+")("+finals+")[1-5]?|("+standalones+")[1-5]?)"

pinyin_re = pinyin_re_sub()
pinyin_two_re = re.compile("(?P<one>"+pinyin_re+")(?P<two>"+pinyin_re+")", flags=re.I)

def jyutping_re_sub():
    inits = "ng|gw|kw|[bpmfdtnlgkhwzcsj]"
    finals = "i|ip|it|ik|im|in|ing|iu|yu|yut|yun|u|up|ut|uk|um|un|ung|ui|e|ep|et|ek|em|en|eng|ei|eu|eot|eon|eoi|oe|oet|oek|oeng|oei|o|ot|ok|om|on|ong|oi|ou|ap|at|ak|am|an|ang|ai|au|aa|aap|aat|aak|aam|aan|aang|aai|aau|m|ng"
    standalones = "'uk|'ung|'e|'ei|'oe|'o|'ok|'om|'on|'ong|'oi|'ou|'ap|'at|'ak|'am|'an|'ang|'ai|'au|'aa|'aap|'aat|'aak|'aam|'aan|'aang|'aai|'aau|'m|'ng"
    return "(("+inits+")("+finals+")[1-6]?|("+standalones+")[1-6]?)"

jyutping_re = jyutping_re_sub()
jyutping_two_re = re.compile("(?P<one>"+jyutping_re+")(?P<two>"+jyutping_re+")", flags=re.I)

db = dictdb.DictDB()

bopomofo_notes = {
 "ˊ":"2", "ˇ":"3","ˋ":"4", "˙":"5"}

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
    elif re.match(".+[¹²³⁴]$", pinyin):
        return str(" ¹²³⁴".index(pinyin[-1:]))
    elif re.match("[\u3100-\u312F]", pinyin):#Bopomofo
        if re.match("[ˊˇˋ˙]", pinyin[-1:]):
            return str("  ˊˇˋ˙".index(pinyin[-1:]))
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
    return re.search("[\u3400-\u9fff]\[.+\]", text)

def has_hanzi(text):
    return re.search("[\u3400-\u9fff]", text)


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
        return re.sub("v", "ü", text)
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

    txt = re.sub("([\u3400-\u9fff|]+)\\[(.*?)\\]", _sub, txt)
    return txt
