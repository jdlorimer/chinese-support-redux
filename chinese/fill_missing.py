# -*- coding: utf-8 -*-
#
# Copyright © 2013 Chris Hatch, <foonugget@gmail.com>
# 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

from aqt.utils import showInfo
from anki.find import Finder
from edit_behavior_model import Sound_fields
from edit_functions import has_field, sound, get_any, set_all
from aqt import mw


def fill_sounds(collection, view_key):
    if view_key == "deckBrowser":
        return showInfo(u"First select one of your decks")

    query_str = "deck:current"

    notes = Finder(collection).findNotes(query_str)
    mw.progress.start(immediate=True)
    for noteId in notes:
        note = collection.getNote(noteId)
        note_dict = dict(note)      # edit_function routines require a dict
        if has_field(Sound_fields, note_dict) and \
                get_any(Sound_fields, note_dict)=="":
            set_all(Sound_fields, note_dict, to = sound(note_dict["Hanzi"]))
            
            # write back to note from dict and flush
            for f in Sound_fields:
                if note_dict.has_key(f) and note_dict[f] <> note[f]:
                    note[f] = note_dict[f]
                    note.flush()
    mw.progress.finish()

def fill_all(collection, view_key):
    # TODO: fill all - reading, pinyin, sounds, etc.
    return


