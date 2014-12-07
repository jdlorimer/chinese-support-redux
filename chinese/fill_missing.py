# -*- coding: utf-8 -*-
#
# Copyright © 2013 Chris Hatch, <foonugget@gmail.com> 
# Copyright © 2014 Thomas TEMPE, <thomas.tempe@alysse.org>
# 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

from aqt.utils import showInfo, askUser
from anki.find import Finder
from edit_behavior import Sound_fields, Hanzi_fields, Transcription_fields, Color_fields, Meaning_fields, Mean_Word_fields, Alternate_fields
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
    if not(askUser("<div>This will update the <i>Sound</i> fields in the current deck, if they are empty.</div>\n\n<div><b>Continue?</b></div>")):
        return False

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
        msg_string = msg_string+"\n\n<div>TTS is taken from an on-line source. It may not always be fully responsive. Please check your network connexion, or retry later.</div>"
    showInfo(msg_string)

#############################################################

def fill_pinyin(collection, view_key):
    if view_key == "deckBrowser":
        return showInfo(u"Please first select one of your decks.")
    if not(askUser("<div>This will update the <i>Pinyin</i> (or <i>Transcription</i>) and <i>Color</i> fields in the current deck.</div>\n\n<div><i>Pinyin</i> and <i>Transcription</i> will only be modified if they are empty.</div>\n\n<div><b>Continue?</b></div>")):
        return False

    query_str = "deck:current"
    d_scanned = 0
    d_has_fields = 0
    d_failed = 0
    d_added_pinyin = 0
    d_updated = 0

    notes = Finder(collection).findNotes(query_str)
    mw.progress.start(immediate=True, min=0, max=len(notes))
    for noteId in notes:
        d_scanned += 1
        note = collection.getNote(noteId)
        note_dict = dict(note)      # edit_function routines require a dict
        if has_field(Transcription_fields, note_dict) and has_field(Hanzi_fields, note_dict):
            d_has_fields += 1

            msg_string = "<b>Processing:</b> %(hanzi)s<br><b>Filled pinyin:</b> %(pinyin)d<br><b>Updated fields:</b>%(updated)d"% {"hanzi":cleanup(no_html(get_any(Hanzi_fields, note_dict))), "pinyin":d_added_pinyin, "updated":d_updated}

            mw.progress.update(label=msg_string, value=d_scanned)

            #Update the transcription field
            #If empty, transcribe from Hanzi
            if get_any(Transcription_fields, note_dict)  == "" :
                t = colorize( transcribe( no_sound( get_any(Hanzi_fields, note_dict) ) ) )
                #Hide the unaccented transcription in the field, 
                #to make searching easier
                t = hide(t, no_tone(t))
                set_all(Transcription_fields, note_dict, to = t )
                if t:
                    d_added_pinyin+=1
            #Otherwise colorize the pinyin
            else:
                t = colorize( accentuate_pinyin( separate_pinyin(no_color(get_any(Transcription_fields, note_dict) ) )))
                t = hide(t, no_tone(t))
                set_all(Transcription_fields, note_dict, to = t)

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
                    d_updated+=1
            for f in Color_fields:
                if note_dict.has_key(f) and note_dict[f] <> note[f]:
                    note[f] = note_dict[f]
                    d_updated+=1
            note.flush()


    mw.progress.finish()
    msg_string = "<b>Processing:</b> %(hanzi)s<br><b>Filled pinyin:</b> %(pinyin)d<br><b>Updated fields:</b>%(updated)d"% {"hanzi":cleanup(no_html(get_any(Hanzi_fields, note_dict))), "pinyin":d_added_pinyin, "updated":d_updated}
    showInfo(msg_string)

############################################################

def fill_translation(collection, view_key):
    if view_key == "deckBrowser":
        return showInfo(u"First select one of your decks")

    if not(askUser("<div>This will update the <i>Meaning</i>, </i>Mean Word, and </i>Also Written</i> fields in the current deck, if they are empty.</div><b>Learning tip:</b><div>Automatic dictionary lookup tends to produce very long text, often with multiple translations.</div>\n\n<div>For more effective memorization, it's highly recommended to trim them down to just a few words, only one meaning, and possibly add some mnemonics.</div>\n\n<div>Dictionary lookup is simply meant as a way to save you time when typing; please consider editing each definition by hand when you're done.</div>\n\n<div><b>Continue?</b></div>")):
        return False

    query_str = "deck:current"
    d_scanned = 0
    d_has_fields = 0
    d_success = 0
    d_failed = 0
    notes = Finder(collection).findNotes(query_str)
    mw.progress.start(immediate=True, min=0, max=len(notes))
    for noteId in notes:
        d_scanned += 1
        note = collection.getNote(noteId)
        note_dict = dict(note)      # edit_function routines require a dict
        if has_field(Meaning_fields, note_dict) and has_field(Hanzi_fields, note_dict):
            d_has_fields += 1

            msg_string = "<b>Processing:</b> %(hanzi)s<br><b>Translated:</b> %(filled)d<br><b>Failed:</b> %(failed)d"% {"hanzi":cleanup(no_html(get_any(Hanzi_fields, note_dict))), "filled":d_success, "failed":d_failed}
            mw.progress.update(label=msg_string, value=d_scanned)

            #Update Meaning field only if empty.
            m = ""
            if get_any(Meaning_fields, note_dict)  == "" :
                m = translate(get_any(Hanzi_fields, note_dict))
                print "Got one", d_success+d_failed, get_any(Hanzi_fields, note_dict), "\t", m
                if not(m): #Translation is empty
                    d_failed+=1
                    print "Failed"
                else: #If there's a translation, then:
                    print "Succeeded"
                    d_success+=1
                    #Mean word
                    _mw = get_mean_word(get_any(Hanzi_fields, note_dict))
                    if _mw:
                        #If there's no mean word field, then add it to the translation
                        if not has_field(Mean_Word_fields, note_dict):
                            m += "<br>Cl: "+_mw
                        else:
                            set_all(Mean_Word_fields, note_dict, to=_mw)
                    _alt = get_alternate_spellings(get_any(Hanzi_fields, note_dict))
                    #Alternate spelling
                    if _alt:
                        #If there's no alt spelling field, then add it to the translation
                        if not has_field(Alternate_fields, note_dict):
                            m += "<br>Also written: "+_mw
                        else:
                            set_all(Alternate_fields, note_dict, to=_alt)
                    set_all(Meaning_fields, note_dict, to = m)
                
        # write back to note from dict and flush
            for f in Meaning_fields:
                if note_dict.has_key(f) and note_dict[f] <> note[f]:
                    note[f] = note_dict[f]
            for f in Mean_Word_fields:
                if note_dict.has_key(f) and note_dict[f] <> note[f]:
                    note[f] = note_dict[f]
            for f in Alternate_fields:
                if note_dict.has_key(f) and note_dict[f] <> note[f]:
                    note[f] = note_dict[f]
            note.flush()
    msg_string = "<b>Translation fill complete</b> %(hanzi)s<br><b>Translated:</b> %(filled)d<br><b>Failed:</b> %(failed)d"% {"hanzi":cleanup(no_html(get_any(Hanzi_fields, note_dict))), "filled":d_success, "failed":d_failed}
    if d_failed>0:
        msg_string = msg_string+"\n\n<div>Translation failures may come either from connection issues (if you're using an on-line translation service), or because some words are not it the dictionary (for local dictionaries).</div>"
    mw.progress.finish()

    showInfo(msg_string)


############################################################

def fill_simp_trad(collection, view_key):
    if view_key == "deckBrowser":
        return showInfo(u"First select one of your decks")
    if not(askUser("<div>This will update the <i>Simplified</i> and <i>Traditional</i> fields in the current deck, if they are empty.</div>\n\n<div><b>Continue?</b></div>")):
        return False

    query_str = "deck:current"
    d_scanned = 0
    d_has_fields = 0
    d_success = 0
    d_failed = 0
    notes = Finder(collection).findNotes(query_str)
    mw.progress.start(immediate=True, min=0, max=len(notes))
    for noteId in notes:
        d_scanned += 1
        note = collection.getNote(noteId)
        note_dict = dict(note)      # edit_function routines require a dict
        if (has_field(Simplified_fields, note_dict) or has_field(Traditional_fields, note_dict)) and has_field(Hanzi_fields, note_dict):
            d_has_fields += 1

            msg_string = "<b>Processing:</b> %(hanzi)s<br><b>Updated:</b> %(filled)d"% {"hanzi":cleanup(no_html(get_any(Hanzi_fields, note_dict))), "filled":d_success}
            mw.progress.update(label=msg_string, value=d_scanned)

            #Update simplified/traditional fields 
            #If it's the same, leave empty, so as to make this feature unobtrusive to simplified chinese users
            s = simplify(field[updated_field])
            if s <> field[updated_field]:
                set_all(Simplified_fields, field, to = s )
            else:
                set_all(Simplified_fields, field, to = "" )
            t = traditional(field[updated_field])
            if t <> field[updated_field]:
                set_all(Traditional_fields, field, to = t )
            else:
                set_all(Traditional_fields, field, to = "" )

        # write back to note from dict and flush
            for f in Traditional_fields:
                if note_dict.has_key(f) and note_dict[f] <> note[f]:
                    note[f] = note_dict[f]
            for f in Simplified_fields:
                if note_dict.has_key(f) and note_dict[f] <> note[f]:
                    note[f] = note_dict[f]
            note.flush()

    msg_string = "<b>Update complete!</b> %(hanzi)s<br><b>Updated:</b> %(filled)d notes"% {"hanzi":cleanup(no_html(get_any(Hanzi_fields, note_dict))), "filled":d_success}
    mw.progress.finish()
    showInfo(msg_string)
