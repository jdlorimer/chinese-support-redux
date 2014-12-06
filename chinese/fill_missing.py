# -*- coding: utf-8 -*-
#
# Copyright © 2013 Chris Hatch, <foonugget@gmail.com> 
# Copyright © 2014 Thomas TEMPE, <thomas.tempe@alysse.org>
# 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

from aqt.utils import showInfo
from anki.find import Finder
from edit_behavior import Sound_fields, Hanzi_fields, Transcription_fields, Color_fields
from edit_functions import *
from aqt import mw
from aqt.utils import showInfo
import re
from time import sleep

def no_html(txt):
    return re.sub("<.*?>", "", txt)

def fill_sounds(collection, view_key):
    if view_key == "deckBrowser":
        return showInfo(u"Please first select one of your decks.")

    query_str = "deck:current"
    d_scanned = 0
    d_has_fields = 0
    d_already_had_sound = 0
    d_success = 0
    d_failed = 0
    notes = Finder(collection).findNotes(query_str)
    mw.progress.start(immediate=True, min=0, max=len(notes))
    for noteId in notes:
        d_scanned += 1
        note = collection.getNote(noteId)
        note_dict = dict(note)      # edit_function routines require a dict
        if has_field(Sound_fields, note_dict) and has_field(Hanzi_fields, note_dict):
            d_has_fields += 1
            if check_for_sound(get_any(Hanzi_fields, note_dict)):
                d_already_had_sound += 1
            else:
                msg_string = "<b>Processing:</b> %(hanzi)s<br><b>OK:</b> %(filled)d<br><b>Failed:</b> %(failed)d"% {"hanzi":cleanup(no_html(get_any(Hanzi_fields, note_dict))), "filled":d_success, "failed":d_failed}
                mw.progress.update(label=msg_string, value=d_scanned)
                s = sound(get_any(Hanzi_fields, note_dict))
                if  "" == s:
                    d_failed = d_failed+1
                    sleep(1)
                else:
                    set_all(Sound_fields, note_dict, to = s)
                    d_success = d_success+1
                # write back to note from dict and flush
                    for f in Sound_fields:
                        if note_dict.has_key(f) and note_dict[f] <> note[f]:
                            note[f] = note_dict[f]
                    note.flush()
    mw.progress.finish()
    msg_string = '''
%(d_success)d new pronunciations downloaded

%(d_failed)d downloads failed

%(have)d/%(d_has_fields)d notes now have pronunciation
''' % {"d_success":d_success, "d_failed":d_failed, "have":d_already_had_sound+d_success, "d_has_fields":d_has_fields}
    if d_failed>0:
        msg_string = msg_string+"\n\nPlease check your network connexion, or retry later."
    showInfo(msg_string)

#############################################################

def fill_pinyin(collection, view_key):
    if view_key == "deckBrowser":
        return showInfo(u"Please first select one of your decks.")

    query_str = "deck:current"
    d_scanned = 0
    d_has_fields = 0
    d_failed = 0
    d_added_pinyin = 0
    d_added_accents = 0

    notes = Finder(collection).findNotes(query_str)
    mw.progress.start(immediate=True, min=0, max=len(notes))
    for noteId in notes:
        d_scanned += 1
        note = collection.getNote(noteId)
        note_dict = dict(note)      # edit_function routines require a dict
        if has_field(Transcription_fields, note_dict) and has_field(Hanzi_fields, note_dict):
            d_has_fields += 1

            msg_string = "<b>Processing:</b> %(hanzi)s<br><b>Filled pinyin:</b> %(pinyin)d<br><b>Added tone marks:</b>%(accents)d"% {"hanzi":cleanup(no_html(get_any(Hanzi_fields, note_dict))), "pinyin":d_added_pinyin, "accents":d_added_accents}
            mw.progress.update(label=msg_string, value=d_scanned)

            #Update the transcription field
            #If empty, transcribe from Hanzi
            if get_any(Transcription_fields, note_dict)  == "" :
                t = colorize( transcribe( no_sound( get_any(Hanzi_fields, note_dict) ) ) )
                #Hide the unaccented transcription in the field, 
                #to make searching easier
                t = hide(t, no_tone(t))
                set_all(Transcription_fields, note_dict, to = t )
                d_added_pinyin+=1
            #Otherwise colorize the pinyin
            else:
                t = colorize( accentuate_pinyin( separate_pinyin(no_color(get_any(Transcription_fields, note_dict) ) )))
                t = hide(t, no_tone(t))
                set_all(Transcription_fields, note_dict, to = t)
                d_added_accents+=1

            #Update Color field from the Hanzi field, 
            #Take the tone info from the Transcription field
            #Always overwrite, as in the default edit_behavior
            h = no_sound( get_any(Hanzi_fields, note_dict) )
            t = no_sound( no_color(get_any(Transcription_fields, note_dict) ) )
            c = colorize_fuse( h, t )
            set_all(Color_fields, note_dict, to = c )

        # write back to note from dict and flush
            for f in Transcription_fields:
                if note_dict.has_key(f) and note_dict[f] <> note[f]:
                    note[f] = note_dict[f]
            for f in Color_fields:
                if note_dict.has_key(f) and note_dict[f] <> note[f]:
                    note[f] = note_dict[f]
            note.flush()


    mw.progress.finish()
    msg_string = "<b>Processing:</b> %(hanzi)s<br><b>Filled pinyin:</b> %(pinyin)d<br><b>Added tone marks:</b>%(accents)d"% {"hanzi":cleanup(no_html(get_any(Hanzi_fields, note_dict))), "pinyin":d_added_pinyin, "accents":d_added_accents}
    showInfo(msg_string)

############################################################

def fill_all(collection, view_key):
    # TODO: fill all - reading, pinyin, sounds, etc.
    return

