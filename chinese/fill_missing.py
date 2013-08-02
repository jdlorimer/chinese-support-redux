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
from aqt.utils import showInfo

def fill_sounds(collection, view_key):
    if view_key == "deckBrowser":
        return showInfo(u"First select one of your decks")

    query_str = "deck:current"
    d_scanned = 0
    d_success = 0
    d_failed = 0
    d_full = 0
    notes = Finder(collection).findNotes(query_str)
    mw.progress.start(immediate=True)
    for noteId in notes:
        d_scanned = d_scanned+1
        note = collection.getNote(noteId)
        note_dict = dict(note)      # edit_function routines require a dict
        if has_field(Sound_fields, note_dict):
            if get_any(Sound_fields, note_dict)=="":
                s = sound(note_dict["Hanzi"])
                if  "" == s:
                    d_failed = d_failed+1
                else:
                    set_all(Sound_fields, note_dict, to = s)
                    d_success = d_success+1
                # write back to note from dict and flush
                for f in Sound_fields:
                    if note_dict.has_key(f) and note_dict[f] <> note[f]:
                        note[f] = note_dict[f]
                        note.flush()
            else:
                d_full = d_full+1
    mw.progress.finish()
    msg_string = "%(empty)d/%(total)d empty Chinese notes in current deck<br>%(filled)d/%(empty)d notes were filled successfully<br>%(failed)d/%(empty)d notes fill failed."% {"empty":d_scanned-d_full, "total":d_scanned, "filled":d_success, "failed":d_failed}
    if d_failed>0:
        msg_string = msg_string+"<br><br>Please check your network connexion, or retry later."
    showInfo(msg_string)

def fill_all(collection, view_key):
    # TODO: fill all - reading, pinyin, sounds, etc.
    return


