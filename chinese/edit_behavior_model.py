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


def update_fields(field, updated_field, model_name, model_type):
    #1st case : the new Ruby-based model
    if model_type == "Chinese support add-ond, word, version.1":
        if updated_field == "Hanzi1":
            field["Hanzi1"] = colorize ( ruby( accentuate_pinyin( field["Hanzi1"] ) ) )
            print "Hanzi1: ", field["Hanzi1"]
            field["Preview"] = hanzi( no_color( field["Hanzi1"] ) )
            field["Meaning"] = translate( field["Hanzi1"] )

    #2nd case : use the old Anki1 Pinyin-toolkit rules if 
    #the deck is called "Chinese" or was created as "Anki1-style from Anki2
    elif model_name == "Chinese" or model_type =="Chinese support add-on, Anki 1-style":
        if updated_field == "Hanzi":
            if field["English"] == "" :
                field["English"] = translate(field["Hanzi"])
            field["Pinyin"] = colorize( transcribe( field["Hanzi"] ) )
            field["Color"] = colorize_fuse(field["Hanzi"], field["Pinyin"])
            mw = mean_word( field["Hanzi"] )
            field["MW"] = colorize( mw + " " + transcribe( mw ) )
            field["Audio"] = audio( field["Hanzi"] )

        elif updated_field == "Pinyin" :
            field["Pinyin"] = colorize(accentuate_pinyin(field["Pinyin"]))
            field["Color"] = colorize_fuse(field["Hanzi"], field["Pinyin"])
            field["Bopomofo"] = transcribe(field["Pinyin"], transcription="Bopomofo")
    return field

