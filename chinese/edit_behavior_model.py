# -*- coding: utf-8 -*-
# Welcome to the Chinese Support Add-on's field edition ruleset.
# Here, you can tweak the note editor helper's behavior to your liking.
#
# If you messed things up, you can safely delete file 
# addons/chinese/edit_behavior.py from your Anki directory.
# It will be recreated the next time you restart Anki.
#
# You can read about all available functions at:
# https://github.com/ttempe/chinese-support-addon/wiki/Edit-behavior
# Also, see the Python tutorial at http://docs.python.org/2/tutorial

from config import chinese_support_config
from edit_functions import *

#Define Variables

anki1_model_names    = ["Chinese", "chinese", "Mandarin Vocab"] #"Mandarin" is used by the Pinyin Toolkit port by Chris Hatch

Hanzi_fields         = ["Expression", "Hanzi", "Chinese",  u"汉字", u"漢字", u"中文"]

#Will use the settings under Tools->Chinese Support->Use local dictionary
Meaning_fields       = ["Meaning", "Definition", u"意思", u"翻译", u"翻譯", u"解释", u"解釋"]

#Will ignore settings and fill regardless
English_fields       = ["English", u"英语", u"英語", u"英文"]
German_fields        = ["German", "Deutsch", u"德语", u"德語", u"德文"]
French_fields        = ["French", "le français", u"法语", u"法語", u"法文"]

#Will use the settings under Tools->Chinese Support->Set Transcription
Transcription_fields = ["Reading"]

#Will ignore settings and fill regardless
Pinyin_fields = ["Pinyin", "PY", u"拼音", u"大陆拼音", u"大陸拼音"]
PinyinTW_fields = ["PinyinTW", "PYTW", u"臺灣拼音", u"台灣拼音", u"台湾拼音"]
Cantonese_fields = ["Cantonese", u"廣東話", u"广东话", u"粵語", u"粤语",u"廣州話", u"广州话", u"粵", u"粤", u"粵拼", u"粤拼"]
Bopomofo_fields = [u"注音符號" u"註音符號", u"注音符号", "Bopomofo", u"ㄅㄆㄇㄈ"]

Sound_fields         = ["Audio", "Sound", "Spoken", u"声音", u"聲音"]

#Will use Google TTS Mandarin regardless of settings
Sound_Mandarin_fields         = ["Sound - Mandarin"]
#Will use Google TTS Cantonese regardless of settings
Sound_Cantonese_fields         = ["Sound - Cantonese"]

Simplified_fields    = ["Simplified", "Simp", "Simp.", u"简体", u"簡體", u"简化", u"簡化", u"简体字", u"簡體字", u"简化字", u"簡化字"]
Traditional_fields   = ["Traditional", "Trad", "Trad.", u"繁体", u"繁體", u"繁体字", u"繁體字"]

Mean_Word_fields     = ["Mean Word", "Measure Word", "MW", "Mean", "Classifier", u"量词", u"量詞"]

Alternate_fields     = ["Also writted", "Alt", "Alternate"]

#Will fill with any Transcription/Pinyin/PinyinTW/Cantonese/Bopomofo field (Transcription fields take highest priority)
Color_fields         = ["Color", "Colour", "Colored Hanzi", "Coloured Hanzi", u"彩色"]

#Will only fill using a Transcription/Pinyin/PinyinTW/Cantonese/Bopomofo field respectively
ColorPY_fields         = ["ColorPY", "ColourPY"]
ColorPYTW_fields         = ["ColorPYTW", "ColourPYTW"]
ColorCANT_fields         = ["ColorCANT", "ColourCANT"]
ColorBPMF_fields         = ["ColorBPMF", "ColourBPMF"]

#Will fill with any Transcription/Pinyin/PinyinTW/Cantonese/Bopomofo field (Transcription fields take highest priority)
Ruby_fields          = ["Ruby"]

#Will only fill using a Transcription/Pinyin/PinyinTW/Cantonese/Bopomofo field respectively
RubyPY_fields          = ["RubyPY"]
RubyPYTW_fields          = ["RubyPYTW"]
RubyCANT_fields          = ["RubyCANT"]
RubyBPMF_fields          = ["RubyBPMF"]

Silhouette_fields    = ["Silhouette"]

#Define Functions

def get_mean(hanzi, dico):

    mw = get_mean_word(hanzi)
    if mw:
        #If there's no mean word field, then add it here
        if not has_field(Mean_Word_fields, dico):
            return "<br>Cl: "+mw
        #Otherwise add it to the mean word field
        elif get_any(Mean_Word_fields, dico)  == "":
            set_all(Mean_Word_fields, dico, to = mw)
    return ""

def get_alt(hanzi, dico):

    alt = get_alternate_spellings(hanzi)
    if alt:
        #If there's no alt spelling field, then add it here
        if not has_field(Alternate_fields, dico):
            return "<br>Also written: "+alt
        #Otherwise add it to the alt spelling field
        elif get_any(Alternate_fields, dico)  == "":
            set_all(Alternate_fields, dico, to = alt )
    return ""
    

#Returns 1 if a translation was found in the dictionary, otherwise returns 0
def update_Meaning_fields(hanzi, dico):

    mw = get_mean(hanzi, dico)
    alt = get_alt(hanzi, dico)
    
    #Update Meaning field only if empty.
    m = ""
    if get_any(Meaning_fields, dico)  == "" :
        m = translate(hanzi)
        if not(m): #Translation is empty
            return 0
        m = m + mw + alt
        set_all(Meaning_fields, dico, to = m)
        
    return 1

def update_English_fields(hanzi, dico):

    mw = get_mean(hanzi, dico)
    alt = get_alt(hanzi, dico)

    #Translate to English
    m = ""
    if get_any(English_fields, dico)  == "" :
        m = translate(hanzi, "zh", "local_en")
        if not(m): #Translation is empty
            return 0
        m = m + mw + alt
        set_all(English_fields, dico, to = m)

    return 1

def update_German_fields(hanzi, dico):

    mw = get_mean(hanzi, dico)
    alt = get_alt(hanzi, dico)

    #Translate to German
    m = ""
    if get_any(German_fields, dico)  == "" :
        m = translate(hanzi, "zh", "local_de")
        if not(m): #Translation is empty
            return 0
        m = m + mw + alt
        set_all(German_fields, dico, to = m)

    return 1

def update_French_fields(hanzi, dico):

    mw = get_mean(hanzi, dico)
    alt = get_alt(hanzi, dico)

    #Translate to French
    m = ""
    if get_any(French_fields, dico)  == "" :
        m = translate(hanzi, "zh", "local_fr")
        if not (m): #Translation is empty
            return 0
        m = m + mw + alt
        set_all(French_fields, dico, to = m)

    return 1

def update_all_Meaning_fields(hanzi, dico):
    update_Meaning_fields(hanzi, dico)
    update_English_fields(hanzi, dico)
    update_German_fields(hanzi, dico)
    update_French_fields(hanzi, dico)
    return

def update_Silhouette_fields(hanzi, dico):
    m = silhouette(hanzi)
    set_all(Silhouette_fields, dico, to = m)
    return

def format_Transcription_fields(dico):
    t = colorize( accentuate_pinyin( separate_pinyin(cleanup(get_any(Transcription_fields, dico)) )))
    t = hide(t, no_tone(t))
    set_all(Transcription_fields, dico, to = t)
    return

#Returns 1 if pinyin was added, otherwise returns 0
def update_Transcription_fields(hanzi, dico):
    #Only if it's empty
    if  get_any(Transcription_fields, dico) == "" :
        t = colorize( transcribe( no_sound( hanzi ) ) )
        #Hide the unaccented transcription in the field, to make searching easier
        t = hide(t, no_tone(t))
        set_all(Transcription_fields, dico, to = t )
        return 1
    #Otherwise colorize and accentuate the existing pinyin
    else:
        format_Transcription_fields(dico)
        return 0

def format_Pinyin_fields(dico):
    t = colorize(accentuate_pinyin(separate_pinyin(cleanup(get_any(Pinyin_fields, dico)), True), True))
    t = hide(t, no_tone(t))
    set_all(Pinyin_fields, dico, to = t)

def update_Pinyin_fields(hanzi, dico):
    if  get_any(Pinyin_fields, dico) == "" :
        t = colorize( transcribe( no_sound( hanzi ), "Pinyin") )
        t = hide(t, no_tone(t))
        set_all(Pinyin_fields, dico, to = t )
        return 1
    else:
        format_Pinyin_fields(dico)
        return 0
    return

def format_PinyinTW_fields(dico):
    t = colorize(accentuate_pinyin(separate_pinyin(cleanup(get_any(PinyinTW_fields, dico)), True), True))
    t = hide(t, no_tone(t))
    set_all(PinyinTW_fields, dico, to = t )

    #Also update Bopomofo
    if has_field(Bopomofo_fields, dico):
        set_all(Bopomofo_fields, dico, to=pinyin_to_bopomofo(t))

    return

def update_PinyinTW_fields(hanzi, dico):
    if  get_any(PinyinTW_fields, dico) == "" :
        t = colorize( transcribe( no_sound( hanzi ), "Pinyin (Taiwan)") )
        t = hide(t, no_tone(t))
        set_all(PinyinTW_fields, dico, to = t )
        return 1
    else:
        format_PinyinTW_fields(dico)
        return 0

def format_Cantonese_fields(dico):
    t = colorize(separate_pinyin(cleanup(get_any(Cantonese_fields, dico)), True, True))
    t = hide(t, no_tone(t))
    set_all(Cantonese_fields, dico, to = t )
    return

def update_Cantonese_fields(hanzi, dico):
    if  get_any(Cantonese_fields, dico) == "" :
        t = colorize( transcribe( no_sound( hanzi ), "Cantonese", False ) )
        t = hide(t, no_tone(t))
        set_all(Cantonese_fields, dico, to = t )
        return 1
    else:
        format_Cantonese_fields(dico)
        return 0

def format_Bopomofo_fields(dico):
    t = colorize(cleanup(get_any(Bopomofo_fields, dico)))
    t = hide(t, no_tone(t))
    set_all(Bopomofo_fields, dico, to = t)
    return

def update_Bopomofo_fields(hanzi, dico):
    if  get_any(Bopomofo_fields, dico) == "" :
        t = colorize( transcribe( no_sound( hanzi ), "Bopomofo") )
        t = hide(t, no_tone(t))
        set_all(Bopomofo_fields, dico, to = t )
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
    return

def update_Color_fields(hanzi, dico):
    #Update Color fields from the Hanzi field,
    h = no_sound( hanzi )
    
    #Take the tone info from the Transcription, Pinyin, PinyinTW, Cantonese or Bopomofo field
    if has_field(Transcription_fields, dico):
        t = no_sound( no_color(get_any(Transcription_fields, dico) ) )
    elif has_field(Pinyin_fields, dico):
        t = no_sound( no_color(get_any(Pinyin_fields, dico) ) )
    elif has_field(PinyinTW_fields, dico):
        t = no_sound( no_color(get_any(PinyinTW_fields, dico) ) )
    elif has_field(Cantonese_fields, dico):
        t = no_sound( no_color(get_any(Cantonese_fields, dico) ) )
    elif has_field(Bopomofo_fields, dico):
        t = no_sound( no_color(get_any(Bopomofo_fields, dico) ) )
    else:
        t = ""
    c = colorize_fuse( h, t )
    set_all(Color_fields, dico, to = c )
    return

def update_ColorPY_fields(hanzi, dico):
    #Update Color fields from the Hanzi field,
    h = no_sound( hanzi )
    
    #Take the tone info from the Pinyin field
    t = no_sound( no_color(get_any(Pinyin_fields, dico) ) )
    c = colorize_fuse( h, t )
    set_all(ColorPY_fields, dico, to = c )
    return

def update_ColorPYTW_fields(hanzi, dico):
    #Update Color fields from the Hanzi field,
    h = no_sound( hanzi )
    
    #Take the tone info from the PinyinTW field
    t = no_sound( no_color(get_any(PinyinTW_fields, dico) ) )
    c = colorize_fuse( h, t )
    set_all(ColorPYTW_fields, dico, to = c )
    return

def update_ColorCANT_fields(hanzi, dico):
    #Update Color fields from the Hanzi field,
    h = no_sound( hanzi )
    
    #Take the tone info from the Cantonese field
    t = no_sound( no_color(get_any(Cantonese_fields, dico) ) )
    c = colorize_fuse( h, t )
    set_all(ColorCANT_fields, dico, to = c )
    return

def update_ColorBPMF_fields(hanzi, dico):
    #Update Color fields from the Hanzi field,
    h = no_sound( hanzi )
    
    #Take the tone info from the Bopomofo field
    t = no_sound( no_color(get_any(Bopomofo_fields, dico) ) )
    c = colorize_fuse( h, t )
    set_all(ColorBPMF_fields, dico, to = c )
    return

def update_all_Color_fields(hanzi, dico):
    update_Color_fields(hanzi, dico)
    update_ColorPY_fields(hanzi, dico)
    update_ColorPYTW_fields(hanzi, dico)
    update_ColorCANT_fields(hanzi, dico)
    update_ColorBPMF_fields(hanzi, dico)
    return

#Returns 1 if a sound was added, otherwise returns 0
def update_Sound_fields(hanzi, dico):
    #Update Sound field from Hanzi field if non-empty
    #(only if field actually exists, as it implies downloading 
    #a soundfile from Internet)
    if has_field(Sound_fields, dico) and \
            get_any(Sound_fields, dico)=="":
        s = sound(hanzi)
        if s:
            set_all(Sound_fields, dico, to = s)
            return 1, 0 #1 field filled, 0 errors
        return 0, 1 
    return 0, 0

def update_Sound_Mandarin_fields(hanzi, dico):
    #Update Sound field from Hanzi field if non-empty
    #(only if field actually exists, as it implies downloading 
    #a soundfile from Internet)
    if has_field(Sound_Mandarin_fields, dico) and \
            get_any(Sound_Mandarin_fields, dico)=="":
        s = sound(hanzi, "Google TTS Mandarin")
        if s:
            set_all(Sound_Mandarin_fields, dico, to = s)
            return 1, 0 #1 field filled, 0 errors
        return 0, 1
    return 0, 0

def update_Sound_Cantonese_fields(hanzi, dico):
    #Update Sound field from Hanzi field if non-empty
    #(only if field actually exists, as it implies downloading 
    #a soundfile from Internet)
    if has_field(Sound_Cantonese_fields, dico) and \
            get_any(Sound_Cantonese_fields, dico)=="":
        s = sound(hanzi, "Google TTS Cantonese")
        if s:
            set_all(Sound_Cantonese_fields, dico, to = s)
            return 1, 0 #1 field filled, 0 errors
        return 0, 1
    return 0, 0

def update_all_Sound_fields(hanzi, dico):
    updated1, errors1 = update_Sound_fields(hanzi, dico)
    updated2, errors2 = update_Sound_Mandarin_fields(hanzi, dico)
    updated3, errors3 = update_Sound_Cantonese_fields(hanzi, dico)
    return updated1+updated2+updated3, errors1+errors2+errors3

def update_Simplified_fields(hanzi, dico):
    
    #Don't do anything if already filled
    if not get_any(Simplified_fields, dico) == "":
        return
    
    s = simplify(hanzi)
    if s <> hanzi:
        set_all(Simplified_fields, dico, to = s )
    else:
        set_all(Simplified_fields, dico, to = "" )
    return

def update_Traditional_fields(hanzi, dico):

    #Don't do anything if already filled
    if not get_any(Traditional_fields, dico) == "":
        return
    
    t = traditional(hanzi)
    if t <> hanzi:
        set_all(Traditional_fields, dico, to = t )
    else:
        set_all(Traditional_fields, dico, to = "" )
    return

def update_Ruby_fields(hanzi, dico):
    #Ruby field will fill as long as either a Transcription, Pinyin, PinyinTW, Cantonese or Bopomofo field exists
    if has_field(Transcription_fields, dico):
        m = colorize_fuse(hanzi, get_any(Transcription_fields, dico), ruby=True)
    elif has_field(Pinyin_fields, dico):
        m = colorize_fuse(hanzi, get_any(Pinyin_fields, dico), ruby=True)
    elif has_field(PinyinTW_fields, dico):
        m = colorize_fuse(hanzi, get_any(PinyinTW_fields, dico), ruby=True)
    elif has_field(Cantonese_fields, dico):
        m = colorize_fuse(hanzi, get_any(Cantonese_fields, dico), ruby=True)
    elif has_field(Bopomofo_fields, dico):
        m = colorize_fuse(hanzi, get_any(Bopomofo_fields, dico), ruby=True)
    else:
        m = ""
    set_all(Ruby_fields, dico, to = m)
    return

def update_RubyPY_fields(hanzi, dico):
    m = colorize_fuse(hanzi, get_any(Pinyin_fields, dico), ruby=True)
    set_all(RubyPY_fields, dico, to = m)
    return

def update_RubyPYTW_fields(hanzi, dico):
    m = colorize_fuse(hanzi, get_any(PinyinTW_fields, dico), ruby=True)
    set_all(RubyPYTW_fields, dico, to = m)
    return

def update_RubyCANT_fields(hanzi, dico):
    m = colorize_fuse(hanzi, get_any(Cantonese_fields, dico), ruby=True)
    set_all(RubyCANT_fields, dico, to = m)
    return

def update_RubyBPMF_fields(hanzi, dico):
    m = colorize_fuse(hanzi, get_any(Bopomofo_fields, dico), ruby=True)
    set_all(RubyBPMF_fields, dico, to = m)
    return


def update_all_Ruby_fields(hanzi, dico):
    update_Ruby_fields(hanzi, dico)
    update_RubyPY_fields(hanzi, dico)
    update_RubyPYTW_fields(hanzi, dico)
    update_RubyCANT_fields(hanzi, dico)
    update_RubyBPMF_fields(hanzi, dico)
    return

def erase_fields(dico):
    set_all(Meaning_fields, dico, to="")
    set_all(English_fields, dico, to="")
    set_all(German_fields, dico, to="")
    set_all(French_fields, dico, to="")
    set_all(Transcription_fields, dico, to="")
    set_all(Pinyin_fields, dico, to="")
    set_all(PinyinTW_fields, dico, to="")
    set_all(Cantonese_fields, dico, to="")
    set_all(Bopomofo_fields, dico, to="")
    set_all(Sound_fields, dico, to="")
    set_all(Simplified_fields, dico, to="")
    set_all(Traditional_fields, dico, to="")
    set_all(Mean_Word_fields, dico, to="")
    set_all(Alternate_fields, dico, to="")
    set_all(Ruby_fields, dico, to="")
    set_all(RubyPY_fields, dico, to="")
    set_all(RubyPYTW_fields, dico, to="")
    set_all(RubyCANT_fields, dico, to="")
    set_all(RubyBPMF_fields, dico, to="")
    set_all(Silhouette_fields, dico, to="")
    set_all(Color_fields, dico, to="")
    set_all(ColorPY_fields, dico, to="")
    set_all(ColorPYTW_fields, dico, to="")
    set_all(ColorCANT_fields, dico, to="")
    set_all(ColorBPMF_fields, dico, to="")
    return


def update_fields(field, updated_field, model_name, model_type):
    #1st case : the new Ruby-based model
    if model_type == "Chinese Ruby":
        if updated_field == "Hanzi":
            #Update the ruby
            h = colorize(ruby(accentuate_pinyin(field["Hanzi"])))
            #Add the toneless transcription and hanzi, hidden, 
            #to make them searchable
            h = hide_ruby(h)
            field["Hanzi"] = h
            if field["Hanzi"] == "":
                field["Meaning"] = ""
            elif field["Meaning"] == "":
                field["Meaning"] = translate( field["Hanzi"] )
        elif updated_field[0:5] == "Hanzi":#Field name starts with "Hanzi"
            field[updated_field] = \
                colorize( ruby( accentuate_pinyin( field[updated_field] ) ) )

    #2nd case : use the old Anki1 Pinyin-toolkit rule1s if the deck is
    #called "Chinese" or was created as "Chinese (compatibility)" from
    #Anki2.
    #Note that we accept multiple field names for each field, to ensure
    #Anki1 compatibility.
    else:

        #Fields to update after the Hanzi field has been modified:
        if updated_field in Hanzi_fields:

            #Erase other fields if the updated field was emptied
            if field[updated_field]=="":
                erase_fields(field)
            else:
                update_all_Meaning_fields(field[updated_field], field)
                update_all_Transcription_fields(field[updated_field], field)
                update_all_Color_fields(field[updated_field], field)
                update_all_Sound_fields(field[updated_field], field)
                update_Simplified_fields(field[updated_field], field)
                update_Traditional_fields(field[updated_field], field)
                update_all_Ruby_fields(field[updated_field], field)
                update_Silhouette_fields(field[updated_field], field)

        #If the transcription was modified, update the Color field
        elif updated_field in Transcription_fields:
            hanzi = get_any(Hanzi_fields, field)
            format_Transcription_fields(field)
            update_all_Color_fields(hanzi, field)
            update_all_Ruby_fields(hanzi, field)

        elif updated_field in Pinyin_fields:
            hanzi = get_any(Hanzi_fields, field)
            format_Pinyin_fields(field)
            update_all_Color_fields(hanzi, field)
            update_all_Ruby_fields(hanzi, field)

        elif updated_field in PinyinTW_fields:
            hanzi = get_any(Hanzi_fields, field)
            format_PinyinTW_fields(field)
            update_all_Color_fields(hanzi, field)
            update_all_Ruby_fields(hanzi, field)

        elif updated_field in Cantonese_fields:
            hanzi = get_any(Hanzi_fields, field)
            format_Cantonese_fields(field)
            update_all_Color_fields(hanzi, field)
            update_all_Ruby_fields(hanzi, field)

        elif updated_field in Bopomofo_fields:
            hanzi = get_any(Hanzi_fields, field)
            format_Bopomofo_fields(field)
            update_all_Color_fields(hanzi, field)
            update_all_Ruby_fields(hanzi, field)
                    
    return field
