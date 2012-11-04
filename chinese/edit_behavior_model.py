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
from edit_functions import *

anki1_model_names = ["Chinese", "chinese", "Mandarin Vocab"]
Hanzi_fields      = ["Expression", "Hanzi", "Chinese",  u"汉字", u"中文"]
Color_fields      = ["Color", "Colour", "Colored Hanzi", u"彩色"]
Reading_fields    = ["Reading", "Pinyin", "PY", u"拼音"]
Meaning_fields    = ["Meaning", "Definition", "English", "German", "French", u"意思", u"翻译", u"英语", u"法语", u"德语"]


def update_fields(field, updated_field, model_name, model_type):
    #1st case : the new Ruby-based model
    if model_type == "Chinese Ruby":
        if updated_field == "Hanzi":
            field["Hanzi"] = colorize(ruby(accentuate_pinyin(field["Hanzi"])))
            field["Preview"] = hanzi( no_color( field["Hanzi"] ) )
            field["Meaning"] = translate( field["Hanzi"] )
        if updated_field == "Hanzi2":
            field["Hanzi2"] = \
                colorize( ruby( accentuate_pinyin( field["Hanzi2"] ) ) )
        if updated_field == "Hanzi3":
            field["Hanzi3"] = \
                colorize( ruby( accentuate_pinyin( field["Hanzi3"] ) ) )
        if updated_field == "Hanzi4":
            field["Hanzi4"] = \
                colorize( ruby( accentuate_pinyin( field["Hanzi4"] ) ) )

    #2nd case : use the old Anki1 Pinyin-toolkit rules if the deck is
    #called "Chinese" or was created as "Chinese (compatibility)" from
    #Anki2.
    #Note that we accept multiple field names for each field, to ensure
    #Anki1 compatibility.
    elif model_name in anki1_model_names \
            or model_type =="Chinese (compatibility)":   
        if updated_field in Hanzi_fields:
            #Update Meaning field only if empty
            if get_any(Meaning_fields, field)  == "" :
                set_all(Meaning_fields, field, \
                            to = translate(field[updated_field]))
            set_all(Reading_fields, field, \
                        to = colorize( transcribe( field[updated_field] ) ) )
            set_all(Color_fields, field, \
                    to = colorize_fuse( field[updated_field], \
                               no_color(get_any(Reading_fields, field) ) ) )
        elif updated_field in Reading_fields:
            field[updated_field] = \
                colorize( accentuate_pinyin( field[updated_field] ) )
            set_all(Color_fields, field, \
                    to = colorize_fuse( get_any( Hanzi_fields, field),\
                        no_color( field[updated_field] ) ) ) 
                    
    return field

