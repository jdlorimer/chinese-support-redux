# Copyright 2013 Chris Hatch <foonugget@gmail.com>
# Copyright 2014 Thomas TEMPE <thomas.tempe@alysse.org>
# Copyright 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from time import sleep
import re

from anki.find import Finder
from aqt import mw
from aqt.utils import showInfo, askUser

from .edit_behavior import *
from .edit_functions import *
from .main import config_manager as config


def no_html(txt):
    return re.sub("<.*?>", "", txt)


def fill_sounds():
    prompt = '''<div>This will update the <i>Sound</i> fields in the current
                deck, if they exist and are empty, using the selected speech
                engine.</div>
                <div>Please back-up your Anki deck first!</div>
                <div>(Please also note that there will be a 5 second delay
                between each sound request, to reduce burden on the server.
                This may therefore take a while.)</div>
                <div><b>Continue?</b></div>'''

    if not askUser(prompt):
        return False

    query_str = "deck:current"
    d_scanned = 0
    d_has_fields = 0
    d_already_had_sound = 0
    d_success = 0
    d_failed = 0

    notes = Finder(mw.col).findNotes(query_str)
    mw.progress.start(immediate=True, min=0, max=len(notes))
    for noteId in notes:
        d_scanned += 1
        note = mw.col.getNote(noteId)
        note_dict = dict(note)      # edit_function routines require a dict

        _hf_s = has_field(config.options['fields']['sound'], note_dict)
        _hf_sm = has_field(config.options['fields']['mandarinSound'], note_dict)
        _hf_sc = has_field(config.options['fields']['cantoneseSound'], note_dict)

        if (_hf_s or _hf_sm or _hf_sc) and has_field(config.options['fields']['hanzi'], note_dict):
            d_has_fields += 1

            hanzi = get_any(config.options['fields']['hanzi'], note_dict)

            if get_any(config.options['fields']['sound'], note_dict) or get_any(config.options['fields']['mandarinSound'], note_dict) or get_any(config.options['fields']['cantoneseSound'], note_dict):
                d_already_had_sound += 1
            else:
                msg_string = "<b>Processing:</b> %(hanzi)s<br><b>Updated:</b> %(d_success)d notes<br><b>Failed:</b> %(d_failed)d notes"% {"hanzi":cleanup(no_html(get_any(config.options['fields']['hanzi'], note_dict))), "d_success":d_success, "d_failed":d_failed}
                mw.progress.update(label=msg_string, value=d_scanned)
                s, f = update_all_Sound_fields(hanzi, note_dict)
                d_success += s
                d_failed += f

                # write back to note from dict and flush
                for f in config.options['fields']['sound'] + config.options['fields']['mandarinSound'] + config.options['fields']['cantoneseSound']:
                    if f in note_dict and note_dict[f] != note[f]:
                        note[f] = note_dict[f]
                note.flush()
                sleep(5)

    mw.progress.finish()
    msg_string = '''
%(d_success)d new pronunciations downloaded

%(d_failed)d downloads failed

%(have)d/%(d_has_fields)d notes now have pronunciation
''' % {"d_success":d_success, "d_failed":d_failed, "have":d_already_had_sound+d_success, "d_has_fields":d_has_fields}
    if d_failed>0:
        msg_string = msg_string+"\n\nTTS is taken from an on-line source. It may not always be fully responsive. Please check your network connexion, or retry later."
    showInfo(msg_string)

#############################################################

def fill_pinyin():
    if not(askUser("<div>This will update the <i>Pinyin</i> (or <i>Transcription</i>), <i>Color</i> and <i>Ruby</i> fields in the current deck, if they exist.</div>\n\n<div><i>Pinyin</i> and <i>Transcription</i> will be filled if empty. Otherwise, their colorization and accentuation will be refreshed as needed.</div>\n\n<div>Please back-up your Anki deck first!</div>\n\n<div><b>Continue?</b></div>")):
        return False

    query_str = "deck:current"
    d_scanned = 0
    d_has_fields = 0
    d_failed = 0
    d_added_pinyin = 0
    d_updated = 0

    notes = Finder(mw.col).findNotes(query_str)
    mw.progress.start(immediate=True, min=0, max=len(notes))
    for noteId in notes:
        d_scanned += 1
        note = mw.col.getNote(noteId)
        note_dict = dict(note)      # edit_function routines require a dict

        _hf_t = has_field(config.options['fields']['transcription'], note_dict)
        _hf_py = has_field(config.options['fields']['pinyin'], note_dict)
        _hf_pytw = has_field(config.options['fields']['pinyinTaiwan'], note_dict)
        _hf_cant = has_field(config.options['fields']['cantonese'], note_dict)
        _hf_bpmf = has_field(config.options['fields']['bopomofo'], note_dict)

        if (_hf_t or _hf_py or _hf_pytw or _hf_cant or _hf_bpmf) and has_field(config.options['fields']['hanzi'], note_dict):
            d_has_fields += 1

            msg_string = "<b>Processing:</b> %(hanzi)s<br><b>Filled pinyin:</b> %(pinyin)d notes<br><b>Updated: </b>%(updated)d fields"% {"hanzi":cleanup(no_html(get_any(config.options['fields']['hanzi'], note_dict))), "pinyin":d_added_pinyin, "updated":d_updated}
            mw.progress.update(label=msg_string, value=d_scanned)

            hanzi = get_any(config.options['fields']['hanzi'], note_dict)
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
                    if f in note_dict and note_dict[f] != note[f]:
                        note[f] = note_dict[f]
                        num_updated+=1
                return num_updated

            # write back to note from dict and flush
            d_updated += write_back(config.options['fields']['transcription'])
            d_updated += write_back(config.options['fields']['pinyin'])
            d_updated += write_back(config.options['fields']['pinyinTaiwan'])
            d_updated += write_back(config.options['fields']['cantonese'])
            d_updated += write_back(config.options['fields']['bopomofo'])
            d_updated += write_back(config.options['fields']['color'])
            d_updated += write_back(config.options['fields']['colorPinyin'])
            d_updated += write_back(config.options['fields']['colorPinyinTaiwan'])
            d_updated += write_back(config.options['fields']['colorCantonese'])
            d_updated += write_back(config.options['fields']['colorBopomofo'])
            d_updated += write_back(config.options['fields']['ruby'])
            d_updated += write_back(config.options['fields']['rubyPinyin'])
            d_updated += write_back(config.options['fields']['rubyPinyinTaiwan'])
            d_updated += write_back(config.options['fields']['rubyCantonese'])
            d_updated += write_back(config.options['fields']['rubyBopomofo'])
            note.flush()


    mw.progress.finish()
    msg_string = "<b>Processing:</b> %(hanzi)s<br><b>Filled pinyin:</b> %(pinyin)d notes<br><b>Updated: </b>%(updated)d fields"% {"hanzi":cleanup(no_html(get_any(config.options['fields']['hanzi'], note_dict))), "pinyin":d_added_pinyin, "updated":d_updated}
    showInfo(msg_string)

############################################################

def fill_translation():
    if not(askUser("<div>This will update the <i>Meaning</i>, <i>Mean Word</i>, and <i>Also Written</i> fields in the current deck, if they exist and are empty.</div><b>Learning tip:</b><div>Automatic dictionary lookup tends to produce very long text, often with multiple translations.</div>\n\n<div>For more effective memorization, it's highly recommended to trim them down to just a few words, only one meaning, and possibly add some mnemonics.</div>\n\n<div>Dictionary lookup is simply meant as a way to save you time when typing; please consider editing each definition by hand when you're done.</div>\n\n<div>Please back-up your Anki deck first!</div>\n\n<div><b>Continue?</b></div>")):
        return False

    query_str = "deck:current"
    d_scanned = 0
    d_has_fields = 0
    d_success = 0
    d_failed = 0
    failed_hanzi = []
    notes = Finder(mw.col).findNotes(query_str)
    mw.progress.start(immediate=True, min=0, max=len(notes))
    for noteId in notes:
        d_scanned += 1
        note = mw.col.getNote(noteId)
        note_dict = dict(note)      # edit_function routines require a dict

        _hf_m = has_field(config.options['fields']['meaning'], note_dict)
        _hf_e = has_field(config.options['fields']['english'], note_dict)
        _hf_g = has_field(config.options['fields']['german'], note_dict)
        _hf_f = has_field(config.options['fields']['french'], note_dict)

        if (_hf_m or _hf_e or _hf_g or _hf_f) and has_field(config.options['fields']['hanzi'], note_dict):
            d_has_fields += 1

            msg_string = "<b>Processing:</b> %(hanzi)s<br><b>Chinese notes:</b> %(has_fields)d<br><b>Translated:</b> %(filled)d<br><b>Failed:</b> %(failed)d"% {"hanzi":cleanup(no_html(get_any(config.options['fields']['hanzi'], note_dict))), "has_fields":d_has_fields, "filled":d_success, "failed":d_failed}
            mw.progress.update(label=msg_string, value=d_scanned)

            hanzi = get_any(config.options['fields']['hanzi'], note_dict)
            empty = len(get_any(config.options['fields']['meaning'], note_dict))
            empty += len(get_any(config.options['fields']['english'], note_dict))
            empty += len(get_any(config.options['fields']['german'], note_dict))
            empty += len(get_any(config.options['fields']['french'], note_dict))
            if not(empty):
                result=0
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
                    if d_failed<20:
                        failed_hanzi += [cleanup(no_html(get_any(config.options['fields']['hanzi'], note_dict)))]
                else:
                    d_success+=1

            def write_back(fields):
                for f in fields:
                    if f in note_dict and note_dict[f] != note[f]:
                        note[f] = note_dict[f]
                return

            # write back to note from dict and flush
            write_back(config.options['fields']['meaning'])
            write_back(config.options['fields']['english'])
            write_back(config.options['fields']['german'])
            write_back(config.options['fields']['french'])
            write_back(config.options['fields']['classifier'])
            write_back(config.options['fields']['alternative'])
            note.flush()

    msg_string = "<b>Translation complete</b> <br><b>Chinese notes:</b> %(has_fields)d<br><b>Translated:</b> %(filled)d<br><b>Failed:</b> %(failed)d"% {"has_fields":d_has_fields, "filled":d_success, "failed":d_failed}
    if d_failed>0:
        msg_string += "\n\n<div>Translation failures may come either from connection issues (if you're using an on-line translation service), or because some words are not it the dictionary (for local dictionaries).</div>"
        msg_string += "<div>The following notes failed: "+ ", ".join(failed_hanzi)+"</div>"
    mw.progress.finish()

    showInfo(msg_string)


############################################################

def fill_simp_trad():
    if not(askUser("<div>This will update the <i>Simplified</i> and <i>Traditional</i> fields in the current deck, if they exist and are empty.</div>\n\n<div>Please back-up your Anki deck first!</div>\n\n<div><b>Continue?</b></div>")):
        return False

    query_str = "deck:current"
    d_scanned = 0
    d_has_fields = 0
    d_success = 0
    d_failed = 0
    notes = Finder(mw.col).findNotes(query_str)
    mw.progress.start(immediate=True, min=0, max=len(notes))
    for noteId in notes:
        d_scanned += 1
        note = mw.col.getNote(noteId)
        note_dict = dict(note)      # edit_function routines require a dict
        if (has_field(config.options['fields']['simplified'], note_dict) or has_field(config.options['fields']['traditional'], note_dict)) and has_field(config.options['fields']['hanzi'], note_dict):
            d_has_fields += 1

            msg_string = "<b>Processing:</b> %(hanzi)s<br><b>Updated:</b> %(filled)d"% {"hanzi":cleanup(no_html(get_any(config.options['fields']['hanzi'], note_dict))), "filled":d_success}
            mw.progress.update(label=msg_string, value=d_scanned)

            #Update simplified/traditional fields
            #If it's the same, leave empty,
            #so as to make this feature unobtrusive to simplified chinese users
            hanzi = get_any(config.options['fields']['hanzi'], note_dict)

            update_Simplified_fields(hanzi, note_dict)
            update_Traditional_fields(hanzi, note_dict)

            # write back to note from dict and flush
            for f in config.options['fields']['traditional']:
                if f in note_dict and note_dict[f] != note[f]:
                    note[f] = note_dict[f]
                    d_success+=1
            for f in config.options['fields']['simplified']:
                if f in note_dict and note_dict[f] != note[f]:
                    note[f] = note_dict[f]
                    d_success+=1
            note.flush()

    msg_string = "<b>Update complete!</b> %(hanzi)s<br><b>Updated:</b> %(filled)d notes"% {"hanzi":cleanup(no_html(get_any(config.options['fields']['hanzi'], note_dict))), "filled":d_success}
    mw.progress.finish()
    showInfo(msg_string)


############################################################

def fill_silhouette():
    if not(askUser("<div>This will update the <i>Silhouette</i> fields in the current deck.</div>\n\n<div>Please back-up your Anki deck first!</div>\n\n<div><b>Continue?</b></div>")):
        return False

    query_str = "deck:current"
    d_scanned = 0
    d_has_fields = 0
    d_success = 0
    d_failed = 0
    notes = Finder(mw.col).findNotes(query_str)
    mw.progress.start(immediate=True, min=0, max=len(notes))
    for noteId in notes:
        d_scanned += 1
        note = mw.col.getNote(noteId)
        note_dict = dict(note)      # edit_function routines require a dict
        if has_field(config.options['fields']['silhouette'], note_dict):
            d_has_fields += 1

            msg_string = "<b>Processing:</b> %(hanzi)s<br><b>Updated:</b> %(filled)d"% {"hanzi":cleanup(no_html(get_any(config.options['fields']['hanzi'], note_dict))), "filled":d_success}
            mw.progress.update(label=msg_string, value=d_scanned)

            hanzi = get_any(config.options['fields']['hanzi'], note_dict)

            #Update Silhouette
            update_Silhouette_fields(hanzi, note_dict)

            # write back to note from dict and flush
            for f in config.options['fields']['silhouette']:
                if f in note_dict and note_dict[f] != note[f]:
                    note[f] = note_dict[f]
                    d_success+=1
            note.flush()

    msg_string = "<b>Update complete!</b> %(hanzi)s<br><b>Updated:</b> %(filled)d notes"% {"hanzi":cleanup(no_html(get_any(config.options['fields']['hanzi'], note_dict))), "filled":d_success}
    mw.progress.finish()
    showInfo(msg_string)
