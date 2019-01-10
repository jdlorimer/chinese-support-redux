# Copyright © 2013 Chris Hatch <foonugget@gmail.com>
# Copyright © 2014 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2019 Joseph Lorimer <luoliyan@posteo.net>
#
# This file is part of Chinese Support Redux.
#
# Chinese Support Redux is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Chinese Support Redux is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Chinese Support Redux.  If not, see <https://www.gnu.org/licenses/>.


from time import sleep

from anki.find import Finder
from aqt import mw
from aqt.utils import showInfo, askUser

from .behavior import (
    fill_all_defs,
    fill_all_rubies,
    fill_bopomofo,
    fill_color,
    fill_silhouette,
    fill_simp,
    fill_sound,
    fill_trad,
    fill_transcription,
)
from .main import config
from .util import cleanup, get_first, has_field, no_html


PROMPT_TEMPLATE = (
    '<div>This will update the {field_names} fields in the current deck.</div>'
    '<div>Please back-up your Anki deck first!</div>'
    '{extra_info}'
    '<div><b>Continue?</b></div>'
)


def bulk_fill_sound():
    extra = (
        '<div>There will be a 5 second delay between each sound request,'
        ' so this may take a while.</div>'
    )
    prompt = PROMPT_TEMPLATE.format(
        field_names='<i>Sound</i>', extra_info=extra
    )

    if not askUser(prompt):
        return

    query_str = 'deck:current'
    d_scanned = 0
    d_has_fields = 0
    d_already_had_sound = 0
    d_success = 0
    d_failed = 0

    note_ids = Finder(mw.col).findNotes(query_str)
    mw.progress.start(immediate=True, min=0, max=len(note_ids))
    for nid in note_ids:
        d_scanned += 1
        orig = mw.col.getNote(nid)
        copy = dict(orig)

        _hf_s = has_field(config['fields']['sound'], copy)
        _hf_sm = has_field(config['fields']['mandarinSound'], copy)
        _hf_sc = has_field(config['fields']['cantoneseSound'], copy)

        if (_hf_s or _hf_sm or _hf_sc) and has_field(
            config['fields']['hanzi'], copy
        ):
            d_has_fields += 1

            hanzi = get_first(config['fields']['hanzi'], copy)

            if (
                get_first(config['fields']['sound'], copy)
                or get_first(config['fields']['mandarinSound'], copy)
                or get_first(config['fields']['cantoneseSound'], copy)
            ):
                d_already_had_sound += 1
            else:
                msg = '''
                <b>Processing:</b> %(hanzi)s<br>
                <b>Updated:</b> %(d_success)d notes<br>
                <b>Failed:</b> %(d_failed)d notes''' % {
                    'hanzi': sanitize_hanzi(copy),
                    'd_success': d_success,
                    'd_failed': d_failed,
                }
                mw.progress.update(label=msg, value=d_scanned)
                s, f = fill_sound(hanzi, copy)
                d_success += s
                d_failed += f
                save_note(orig, copy)
                sleep(5)

    mw.progress.finish()
    msg = '''
%(d_success)d new pronunciations downloaded

%(d_failed)d downloads failed

%(have)d/%(d_has_fields)d notes now have pronunciation''' % {
        'd_success': d_success,
        'd_failed': d_failed,
        'have': d_already_had_sound + d_success,
        'd_has_fields': d_has_fields,
    }
    if d_failed > 0:
        msg += (
            'TTS is taken from an online source. '
            'It may not always be fully responsive. '
            'Please check your network connexion, or retry later.'
        )
    showInfo(msg)


def save_note(orig, copy):
    for f in orig.keys():
        if f in copy and copy[f] != orig[f]:
            orig[f] = copy[f]
    orig.flush()


def bulk_fill_pinyin():

    prompt = PROMPT_TEMPLATE.format(
        field_names='<i>transcription</i> and <i>ruby</i>', extra_info=''
    )

    if not askUser(prompt):
        return

    query_str = 'deck:current'
    d_scanned = 0
    d_has_fields = 0
    d_added_pinyin = 0
    d_updated = 0

    notes = Finder(mw.col).findNotes(query_str)
    mw.progress.start(immediate=True, min=0, max=len(notes))
    for noteId in notes:
        d_scanned += 1
        note = mw.col.getNote(noteId)
        note_dict = dict(note)

        _hf_t = has_field(config['fields']['transcription'], note_dict)
        _hf_py = has_field(config['fields']['pinyin'], note_dict)
        _hf_pytw = has_field(config['fields']['pinyinTaiwan'], note_dict)
        _hf_cant = has_field(config['fields']['cantonese'], note_dict)
        _hf_bpmf = has_field(config['fields']['bopomofo'], note_dict)

        if (_hf_t or _hf_py or _hf_pytw or _hf_cant or _hf_bpmf) and has_field(
            config['fields']['hanzi'], note_dict
        ):
            d_has_fields += 1

            msg = '''
            <b>Processing:</b> %(hanzi)s<br>
            <b>Filled pinyin:</b> %(pinyin)d notes<br>
            <b>Updated: </b>%(updated)d fields''' % {
                'hanzi': sanitize_hanzi(note_dict),
                'pinyin': d_added_pinyin,
                'updated': d_updated,
            }
            mw.progress.update(label=msg, value=d_scanned)

            hanzi = get_first(config['fields']['hanzi'], note_dict)
            results = 0

            if _hf_t:
                results += fill_transcription(hanzi, note_dict)
            if _hf_bpmf:
                results += fill_bopomofo(hanzi, note_dict)

            if results != 0:
                d_added_pinyin += 1

            fill_color(hanzi, note_dict)
            fill_all_rubies(hanzi, note_dict)

            def write_back(fields):
                num_updated = 0
                for f in fields:
                    if f in note_dict and note_dict[f] != note[f]:
                        note[f] = note_dict[f]
                        num_updated += 1
                return num_updated

            d_updated += write_back(config['fields']['transcription'])
            d_updated += write_back(config['fields']['pinyin'])
            d_updated += write_back(config['fields']['pinyinTaiwan'])
            d_updated += write_back(config['fields']['cantonese'])
            d_updated += write_back(config['fields']['bopomofo'])
            d_updated += write_back(config['fields']['color'])
            d_updated += write_back(config['fields']['colorPinyin'])
            d_updated += write_back(config['fields']['colorPinyinTaiwan'])
            d_updated += write_back(config['fields']['colorCantonese'])
            d_updated += write_back(config['fields']['colorBopomofo'])
            d_updated += write_back(config['fields']['ruby'])
            d_updated += write_back(config['fields']['rubyPinyin'])
            d_updated += write_back(config['fields']['rubyPinyinTaiwan'])
            d_updated += write_back(config['fields']['rubyCantonese'])
            d_updated += write_back(config['fields']['rubyBopomofo'])
            note.flush()

    mw.progress.finish()
    msg = '''
    <b>Processing:</b> %(hanzi)s<br>
    <b>Filled pinyin:</b> %(pinyin)d notes<br>
    <b>Updated: </b>%(updated)d fields''' % {
        'hanzi': sanitize_hanzi(note_dict),
        'pinyin': d_added_pinyin,
        'updated': d_updated,
    }
    showInfo(msg)


def bulk_fill_defs():
    prompt = PROMPT_TEMPLATE.format(
        field_names='<i>definition</i>, <i>classifier</i> and <i>alternative</i>',
        extra_info='',
    )

    if not askUser(prompt):
        return

    query_str = 'deck:current'
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
        note_dict = dict(note)

        _hf_m = has_field(config['fields']['meaning'], note_dict)
        _hf_e = has_field(config['fields']['english'], note_dict)
        _hf_g = has_field(config['fields']['german'], note_dict)
        _hf_f = has_field(config['fields']['french'], note_dict)

        if (_hf_m or _hf_e or _hf_g or _hf_f) and has_field(
            config['fields']['hanzi'], note_dict
        ):
            d_has_fields += 1

            msg = '''
            <b>Processing:</b> %(hanzi)s<br>
            <b>Chinese notes:</b> %(has_fields)d<br>
            <b>Translated:</b> %(filled)d<br>
            <b>Failed:</b> %(failed)d''' % {
                'hanzi': sanitize_hanzi(note_dict),
                'has_fields': d_has_fields,
                'filled': d_success,
                'failed': d_failed,
            }
            mw.progress.update(label=msg, value=d_scanned)

            hanzi = get_first(config['fields']['hanzi'], note_dict)
            empty = len(get_first(config['fields']['meaning'], note_dict))
            empty += len(get_first(config['fields']['english'], note_dict))
            empty += len(get_first(config['fields']['german'], note_dict))
            empty += len(get_first(config['fields']['french'], note_dict))

            if not empty:
                result = fill_all_defs(hanzi, note_dict)

                if result:
                    d_success += 1
                else:
                    d_failed += 1
                    if d_failed < 20:
                        failed_hanzi += [sanitize_hanzi(note_dict)]

            def write_back(fields):
                for f in fields:
                    if f in note_dict and note_dict[f] != note[f]:
                        note[f] = note_dict[f]

            write_back(config['fields']['meaning'])
            write_back(config['fields']['english'])
            write_back(config['fields']['german'])
            write_back(config['fields']['french'])
            write_back(config['fields']['classifier'])
            write_back(config['fields']['alternative'])
            note.flush()

    msg = '''
    <b>Translation complete</b><br>
    <b>Chinese notes:</b> %(has_fields)d<br>
    <b>Translated:</b> %(filled)d<br>
    <b>Failed:</b> %(failed)d''' % {
        'has_fields': d_has_fields,
        'filled': d_success,
        'failed': d_failed,
    }
    if d_failed > 0:
        msg += (
            '<div>Translation failures may come either from connection issues '
            "(if you're using an online translation service), or because some "
            'words are not it the dictionary (for local dictionaries).</div>'
            '<div>The following notes failed: '
            + ', '.join(failed_hanzi)
            + '</div>'
        )
    mw.progress.finish()
    showInfo(msg)


def bulk_fill_hanzi():
    prompt = PROMPT_TEMPLATE.format(field_names='<i>hanzi</i>', extra_info='')

    if not askUser(prompt):
        return

    query_str = 'deck:current'
    d_scanned = 0
    d_has_fields = 0
    d_success = 0
    notes = Finder(mw.col).findNotes(query_str)
    mw.progress.start(immediate=True, min=0, max=len(notes))
    for noteId in notes:
        d_scanned += 1
        note = mw.col.getNote(noteId)
        note_dict = dict(note)
        if (
            has_field(config['fields']['simplified'], note_dict)
            or has_field(config['fields']['traditional'], note_dict)
        ) and has_field(config['fields']['hanzi'], note_dict):
            d_has_fields += 1

            msg = '''
            <b>Processing:</b> %(hanzi)s<br>
            <b>Updated:</b> %(filled)d''' % {
                'hanzi': sanitize_hanzi(note_dict),
                'filled': d_success,
            }
            mw.progress.update(label=msg, value=d_scanned)

            hanzi = get_first(config['fields']['hanzi'], note_dict)

            fill_simp(hanzi, note_dict)
            fill_trad(hanzi, note_dict)

            for f in config['fields']['traditional']:
                if f in note_dict and note_dict[f] != note[f]:
                    note[f] = note_dict[f]
                    d_success += 1

            for f in config['fields']['simplified']:
                if f in note_dict and note_dict[f] != note[f]:
                    note[f] = note_dict[f]
                    d_success += 1

            note.flush()

    msg = '''
    <b>Update complete!</b> %(hanzi)s<br>
    <b>Updated:</b> %(filled)d notes''' % {
        'hanzi': sanitize_hanzi(note_dict),
        'filled': d_success,
    }
    mw.progress.finish()
    showInfo(msg)


def bulk_fill_silhouette():
    prompt = PROMPT_TEMPLATE.format(
        field_names='<i>silhouette</i>', extra_info=''
    )

    if not askUser(prompt):
        return

    query_str = 'deck:current'
    d_scanned = 0
    d_has_fields = 0
    d_success = 0
    notes = Finder(mw.col).findNotes(query_str)
    mw.progress.start(immediate=True, min=0, max=len(notes))
    for noteId in notes:
        d_scanned += 1
        note = mw.col.getNote(noteId)
        note_dict = dict(note)
        if has_field(config['fields']['silhouette'], note_dict):
            d_has_fields += 1
            msg = '''
            <b>Processing:</b> %(hanzi)s<br>
            <b>Updated:</b> %(filled)d''' % {
                'hanzi': sanitize_hanzi(note_dict),
                'filled': d_success,
            }
            mw.progress.update(label=msg, value=d_scanned)
            hanzi = get_first(config['fields']['hanzi'], note_dict)
            fill_silhouette(hanzi, note_dict)

            for f in config['fields']['silhouette']:
                if f in note_dict and note_dict[f] != note[f]:
                    note[f] = note_dict[f]
                    d_success += 1

            note.flush()

    msg = '''
    <b>Update complete!</b> %(hanzi)s<br>
    <b>Updated:</b> %(filled)d notes''' % {
        'hanzi': sanitize_hanzi(note_dict),
        'filled': d_success,
    }
    mw.progress.finish()
    showInfo(msg)


def sanitize_hanzi(note):
    return cleanup(no_html(get_first(config['fields']['hanzi'], note)))
