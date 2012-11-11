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

anki1_model_names    = ["Chinese", "chinese", "Mandarin Vocab"]
Hanzi_fields         = ["Expression", "Hanzi", "Chinese",  u"汉字", u"中文"]
Color_fields         = ["Color", "Colour", "Colored Hanzi", u"彩色"]
Transcription_fields = ["Reading", "Pinyin", "PY", u"拼音"]
Meaning_fields       = ["Meaning", "Definition", "English", "German", \
"French", u"意思", u"翻译", u"英语", u"法语", u"德语", u"法文", u"英文", u"德文"]
Sound_fields         = ["Audio", "Sound", "Spoken", u"声音"]

def update_fields(field, updated_field, model_name, model_type):
    #1st case : the new Ruby-based model
    if model_type == "Chinese Ruby":
        if updated_field == "Hanzi":
            field["Hanzi"] = colorize(ruby(accentuate_pinyin(field["Hanzi"])))
            if field["Hanzi"] == "":
                field["Meaning"] = ""
            elif field["Meaning"] == "":
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

        #Fields to update after the Hanzi field has been modified:
        if updated_field in Hanzi_fields:

            #Update Meaning field only if empty.
            if get_any(Meaning_fields, field)  == "" :
                m = translate(field[updated_field])
                set_all(Meaning_fields, field, to = m)


            #Update transcription field with default transcription (Pinyin?)
            #Only if it's empty
            if get_any(Transcription_fields, field)  == "" :
                t = colorize( transcribe( no_sound( field[updated_field] ) ) )
                set_all(Transcription_fields, field, to = t )

            #Erase other fields if the updated field was emptied
            if field[updated_field]=="":
                set_all(Meaning_fields, field, to="")
                set_all(Transcription_fields, field, to="")
                set_all(Sound_fields, field, to="")


            #Update Color field from the Hanzi field, 
            #Take the tone info from the Transcription field
            h = no_sound( field[updated_field])
            t = no_sound( no_color(get_any(Transcription_fields, field) ) )
            c = colorize_fuse( h, t )
            set_all(Color_fields, field, to = c )

            #Update Sound field from Hanzi field if non-empty
            #(only if field actually exists, as it implies downloading 
            #a soundfile from Internet)
            if has_field(Sound_fields, field) and \
                    get_any(Sound_fields, field)=="":
                set_all(Sound_fields, field, to = sound(field[updated_field]))

        #If the transcription was modified, update the Color field
        elif updated_field in Transcription_fields:
            t = colorize( accentuate_pinyin( field[updated_field] ) )
            field[updated_field] = t
            h = no_sound( get_any( Hanzi_fields, field) )
            t = no_sound( no_color( field[updated_field] ) )
            set_all(Color_fields, field, to = colorize_fuse( h, t ) ) 
                    
    return field

