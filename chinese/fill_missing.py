# -*- coding: utf-8 -*-
#
# Copyright © 2012 Thomas TEMPÉ, <thomas.tempe@alysse.org>
# 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

from aqt.utils import showInfo
from anki.find import Finder
from edit_behavior_model import Sound_fields
from edit_functions import has_field, sound, get_any, set_all

def fill_sounds(collection, view_key):
    if view_key == "deckBrowser":
        return showInfo(u"First select one of your decks")

    query_str = "deck:current"

    # TODO: restrict on note name?? or apply to the whole deck??
    # query_str += " and note:*" + tag + "* "

    notes = Finder(collection).findNotes(query_str)

    for noteId in notes:
        note = collection.getNote(noteId)
        note_dict = dict(note)
        if has_field(Sound_fields, note_dict) and \
                get_any(Sound_fields, note_dict)=="":
            print note["Hanzi"]
#            set_all(Sound_fields, field, to = sound(field[updated_field]))
    
    collection.setMod()

def fill_all(collection, view_key):
    # TODO: fill all - reading, pinyin, sounds, etc.
    return


