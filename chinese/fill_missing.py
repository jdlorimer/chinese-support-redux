# -*- coding: utf-8 -*-
#
# Copyright © 2013 Chris Hatch, <foonugget@gmail.com> 
# Copyright © 2014 Thomas TEMPE, <thomas.tempe@alysse.org>
# 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

from aqt.utils import showInfo, askUser
from anki.find import Finder
from edit_behavior import *
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
    if not(askUser("<div>This will update the <i>Sound</i> fields in the current deck, if they exist and are empty.</div>\n\n<div><b>Continue?</b></div>")):
        return False

    query_str = "deck:current"
    d_scanned = 0
    d_has_fields = 0
    d_already_had_sound = 0
    d_success = 0
    d_failed = 0
    d_downloaded = 0
    d_failed_download = 0
    
    notes = Finder(collection).findNotes(query_str)
    mw.progress.start(immediate=True, min=0, max=len(notes))
    for noteId in notes:
        d_scanned += 1
        note = collection.getNote(noteId)
        note_dict = dict(note)      # edit_function routines require a dict

        _hf_s = has_field(Sound_fields, note_dict)
        _hf_sm = has_field(Sound_Mandarin_fields, note_dict)
        _hf_sc = has_field(Sound_Cantonese_fields, note_dict)

        if (_hf_s or _hf_sm or _hf_sc) and has_field(Hanzi_fields, note_dict):
            d_has_fields += 1

            hanzi = get_any(Hanzi_fields, note_dict)
            
            if check_for_sound(hanzi) and check_for_sound(hanzi + u'(普)') and check_for_sound(hanzi + u'(粵)'):
                d_already_had_sound += 1
            else:
                msg_string = "<b>Processing:</b> %(hanzi)s<br><b>Updated:</b> %(filled)d notes<br><b>Failed:</b> %(failed)d notes"% {"hanzi":cleanup(no_html(get_any(Hanzi_fields, note_dict))), "filled":d_success, "failed":d_failed}
                mw.progress.update(label=msg_string, value=d_scanned)

                _failed = 0

                if _hf_s:
                    if update_Sound_fields(hanzi, note_dict) == 0:
                        d_failed_download += 1
                        _failed = 1
                        sleep(1)
                    else:
                        d_downloaded += 1

                if _hf_sm:
                    if update_Sound_Mandarin_fields(hanzi, note_dict) == 0:
                        d_failed_download += 1
                        _failed = 1
                        sleep(1)
                    else:
                        d_downloaded += 1

                if _hf_sc:
                    if update_Sound_Cantonese_fields(hanzi, note_dict) == 0:
                        d_failed_download += 1
                        _failed = 1
                        sleep(1)
                    else:
                        d_downloaded += 1

                d_failed += _failed

                if _failed == 0:
                    d_success = d_success+1

                # write back to note from dict and flush
                for f in Sound_fields:
                    if note_dict.has_key(f) and note_dict[f] <> note[f]:
                        note[f] = note_dict[f]
                for f in Sound_Mandarin_fields:
                    if note_dict.has_key(f) and note_dict[f] <> note[f]:
                        note[f] = note_dict[f]
                for f in Sound_Cantonese_fields:
                    if note_dict.has_key(f) and note_dict[f] <> note[f]:
                        note[f] = note_dict[f]
                note.flush()
    mw.progress.finish()
    msg_string = '''
%(d_downloaded)d new pronunciations downloaded

%(d_failed_download)d downloads failed

%(have)d/%(d_has_fields)d notes now have pronunciation
''' % {"d_success":d_success, "d_failed":d_failed, "have":d_already_had_sound+d_success, "d_has_fields":d_has_fields, "d_downloaded":d_downloaded, "d_failed_download":d_failed_download}
    if d_failed_download>0:
        msg_string = msg_string+"\n\n<div>TTS is taken from an on-line source. It may not always be fully responsive. Please check your network connexion, or retry later.</div>"
    showInfo(msg_string)

#############################################################

def fill_pinyin(collection, view_key):
    if view_key == "deckBrowser":
        return showInfo(u"Please first select one of your decks.")
    if not(askUser("<div>This will update the <i>Pinyin</i> (or <i>Transcription</i>), <i>Color</i> and <i>Ruby</i> fields in the current deck, if they exist.</div>\n\n<div><i>Pinyin</i> and <i>Transcription</i> will be filled if empty. Otherwise, their colorization and accentuation will be refreshed as needed.</div>\n\n<div><b>Continue?</b></div>")):
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

        _hf_t = has_field(Transcription_fields, note_dict)
        _hf_py = has_field(Pinyin_fields, note_dict)
        _hf_pytw = has_field(PinyinTW_fields, note_dict)
        _hf_cant = has_field(Cantonese_fields, note_dict)
        _hf_bpmf = has_field(Bopomofo_fields, note_dict)
        
        if (_hf_t or _hf_py or _hf_pytw or _hf_cant or _hf_bpmf) and has_field(Hanzi_fields, note_dict):
            d_has_fields += 1

            msg_string = "<b>Processing:</b> %(hanzi)s<br><b>Filled pinyin:</b> %(pinyin)d notes<br><b>Updated: </b>%(updated)d fields"% {"hanzi":cleanup(no_html(get_any(Hanzi_fields, note_dict))), "pinyin":d_added_pinyin, "updated":d_updated}
            mw.progress.update(label=msg_string, value=d_scanned)

            hanzi = get_any(Hanzi_fields, note_dict)
            results = 0

            if _hf_t:
                results += update_Transcription_fields(hanzi, note_dict)
            if _hf_py:
                results += update_Pinyin_fields(hanzi, note_dict)
            if _hf_pytw:
                results += update_PinyinTW_fields(hanzi, note_dict)
            if _hf_cant:
                results += update_Cantonese_fields(hanzi, note_dict)
            if _hf_bpmf:
                results += update_Bopomofo_fields(hanzi, note_dict)

            if results != 0:
                d_added_pinyin+=1

            #Always overwrite, as in the default edit_behavior
            update_all_Color_fields(hanzi, note_dict)           

            #Update ruby field
            update_all_Ruby_fields(hanzi, note_dict)

            def write_back(fields):
                num_updated = 0
                for f in fields:
                    if note_dict.has_key(f) and note_dict[f] <> note[f]:
                        note[f] = note_dict[f]
                        num_updated+=1
                return num_updated

            # write back to note from dict and flush
            d_updated += write_back(Transcription_fields)
            d_updated += write_back(Pinyin_fields)
            d_updated += write_back(PinyinTW_fields)
            d_updated += write_back(Cantonese_fields)
            d_updated += write_back(Bopomofo_fields)
            d_updated += write_back(Color_fields)
            d_updated += write_back(ColorPY_fields)
            d_updated += write_back(ColorPYTW_fields)
            d_updated += write_back(ColorCANT_fields)
            d_updated += write_back(ColorBPMF_fields)
            d_updated += write_back(Ruby_fields)
            d_updated += write_back(RubyPY_fields)
            d_updated += write_back(RubyPYTW_fields)
            d_updated += write_back(RubyCANT_fields)
            d_updated += write_back(RubyBPMF_fields)
            note.flush()


    mw.progress.finish()
    msg_string = "<b>Processing:</b> %(hanzi)s<br><b>Filled pinyin:</b> %(pinyin)d notes<br><b>Updated: </b>%(updated)d fields"% {"hanzi":cleanup(no_html(get_any(Hanzi_fields, note_dict))), "pinyin":d_added_pinyin, "updated":d_updated}
    showInfo(msg_string)

############################################################

def fill_translation(collection, view_key):
    if view_key == "deckBrowser":
        return showInfo(u"First select one of your decks")

    if not(askUser("<div>This will update the <i>Meaning</i>, </i>Mean Word, and </i>Also Written</i> fields in the current deck, if they exist and are empty.</div><b>Learning tip:</b><div>Automatic dictionary lookup tends to produce very long text, often with multiple translations.</div>\n\n<div>For more effective memorization, it's highly recommended to trim them down to just a few words, only one meaning, and possibly add some mnemonics.</div>\n\n<div>Dictionary lookup is simply meant as a way to save you time when typing; please consider editing each definition by hand when you're done.</div>\n\n<div><b>Continue?</b></div>")):
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

        _hf_m = has_field(Meaning_fields, note_dict)
        _hf_e = has_field(English_fields, note_dict)
        _hf_g = has_field(German_fields, note_dict)
        _hf_f = has_field(French_fields, note_dict)
        
        if (_hf_m or _hf_e or _hf_g or _hf_f) and has_field(Hanzi_fields, note_dict):
            d_has_fields += 1

            msg_string = "<b>Processing:</b> %(hanzi)s<br><b>Translated:</b> %(filled)d<br><b>Failed:</b> %(failed)d"% {"hanzi":cleanup(no_html(get_any(Hanzi_fields, note_dict))), "filled":d_success, "failed":d_failed}
            mw.progress.update(label=msg_string, value=d_scanned)

            hanzi = get_any(Hanzi_fields, note_dict)
            result = 0

            if _hf_m:
                result += update_Meaning_fields(hanzi, note_dict)
            if _hf_e:
                result += update_English_fields(hanzi, note_dict)
            if _hf_g:
                result += update_German_fields(hanzi, note_dict)
            if _hf_f:
                result += update_French_fields(hanzi, note_dict)


            if result == 0:
                d_failed+=1
            else:
                d_success+=1

            def write_back(fields):
                for f in fields:
                    if note_dict.has_key(f) and note_dict[f] <> note[f]:
                        note[f] = note_dict[f]
                return

            # write back to note from dict and flush
            write_back(Meaning_fields)
            write_back(English_fields)
            write_back(German_fields)
            write_back(French_fields)                   
            write_back(Mean_Word_fields)
            write_back(Alternate_fields)
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
    if not(askUser("<div>This will update the <i>Simplified</i> and <i>Traditional</i> fields in the current deck, if they exist and are empty.</div>\n\n<div><b>Continue?</b></div>")):
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
            hanzi = get_any(Hanzi_fields, note_dict)

            update_Simplified_fields(hanzi, note_dict)
            update_Traditional_fields(hanzi, note_dict)

            # write back to note from dict and flush
            for f in Traditional_fields:
                if note_dict.has_key(f) and note_dict[f] <> note[f]:
                    note[f] = note_dict[f]
                    d_success+=1
            for f in Simplified_fields:
                if note_dict.has_key(f) and note_dict[f] <> note[f]:
                    note[f] = note_dict[f]
                    d_success+=1
            note.flush()

    msg_string = "<b>Update complete!</b> %(hanzi)s<br><b>Updated:</b> %(filled)d notes"% {"hanzi":cleanup(no_html(get_any(Hanzi_fields, note_dict))), "filled":d_success}
    mw.progress.finish()
    showInfo(msg_string)


############################################################

def fill_silhouette(collection, view_key):
    if view_key == "deckBrowser":
        return showInfo(u"First select one of your decks")
    if not(askUser("<div>This will update the <i>Silhouette</i> fields in the current deck.</div>\n\n<div><b>Continue?</b></div>")):
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
        if has_field(Silhouette_fields, note_dict):
            d_has_fields += 1

            msg_string = "<b>Processing:</b> %(hanzi)s<br><b>Updated:</b> %(filled)d"% {"hanzi":cleanup(no_html(get_any(Hanzi_fields, note_dict))), "filled":d_success}
            mw.progress.update(label=msg_string, value=d_scanned)

            hanzi = get_any(Hanzi_fields, note_dict)

            #Update Silhouette
            update_Silhouette_fields(hanzi, note_dict)

            # write back to note from dict and flush
            for f in Silhouette_fields:
                if note_dict.has_key(f) and note_dict[f] <> note[f]:
                    note[f] = note_dict[f]
                    d_success+=1
            note.flush()

    msg_string = "<b>Update complete!</b> %(hanzi)s<br><b>Updated:</b> %(filled)d notes"% {"hanzi":cleanup(no_html(get_any(Hanzi_fields, note_dict))), "filled":d_success}
    mw.progress.finish()
    showInfo(msg_string)
