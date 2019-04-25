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
from aqt.utils import askUser, showInfo

from .behavior import (
    fill_all_defs,
    fill_all_rubies,
    fill_bopomofo,
    fill_classifier,
    fill_color,
    fill_silhouette,
    fill_simp,
    fill_sound,
    fill_trad,
    fill_transcript,
)
from .hanzi import get_hanzi
from .main import config
from .util import (
    all_fields_empty,
    get_first,
    has_any_field,
    has_field,
    save_note,
)

PROMPT_TEMPLATE = (
    '<div>This will update the {field_names} fields in the current deck.</div>'
    '<div>Please back-up your Anki deck first!</div>'
    '{extra_info}'
    '<div><b>Continue?</b></div>'
)

PROGRESS_TEMPLATE = (
    '<b>Processing:</b> %(hanzi)s<br>'
    '<b>Notes:</b> %(has_fields)d<br>'
    '<b>Filled:</b> %(filled)d<br>'
    '<b>Failed:</b> %(failed)d'
)

END_TEMPLATE = (
    '<b>Bulk filling complete</b><br>'
    '<b>Notes:</b> %(has_fields)d<br>'
    '<b>Filled:</b> %(filled)d<br>'
    '<b>Failed:</b> %(failed)d'
)


def bulk_fill_sound():
    prompt = PROMPT_TEMPLATE.format(
        field_names='<i>Sound</i>',
        extra_info=(
            '<div>There will be a 5 second delay between each sound request,'
            ' so this may take a while.</div>'
        ),
    )

    if not askUser(prompt):
        return

    d_has_fields = 0
    d_already_had_sound = 0
    d_success = 0
    d_failed = 0

    note_ids = Finder(mw.col).findNotes('deck:current')
    mw.progress.start(immediate=True, min=0, max=len(note_ids))

    for i, nid in enumerate(note_ids):
        orig = mw.col.getNote(nid)
        copy = dict(orig)

        if has_any_field(
            copy, ['sound', 'mandarinSound', 'cantoneseSound']
        ) and has_field(config['fields']['hanzi'], copy):
            d_has_fields += 1
            hanzi = get_first(config['fields']['hanzi'], copy)

            if all_fields_empty(
                copy, ['sound', 'mandarinSound', 'cantoneseSound']
            ):
                msg = '''
                <b>Processing:</b> %(hanzi)s<br>
                <b>Updated:</b> %(d_success)d notes<br>
                <b>Failed:</b> %(d_failed)d notes''' % {
                    'hanzi': get_hanzi(copy),
                    'd_success': d_success,
                    'd_failed': d_failed,
                }
                mw.progress.update(label=msg, value=i)
                s, f = fill_sound(hanzi, copy)
                d_success += s
                d_failed += f
                save_note(orig, copy)
                sleep(5)
            else:
                d_already_had_sound += 1

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
            'Please check your network connection, or retry later.'
        )
    showInfo(msg)


def bulk_fill_transcript():
    prompt = PROMPT_TEMPLATE.format(
        field_names='<i>transcription</i> and <i>ruby</i>', extra_info=''
    )

    field_groups = [
        'transcription',
        'pinyin',
        'pinyinTaiwan',
        'cantonese',
        'bopomofo',
    ]

    if not askUser(prompt):
        return

    d_has_fields = 0
    d_added_pinyin = 0
    d_updated = 0

    note_ids = Finder(mw.col).findNotes('deck:current')
    mw.progress.start(immediate=True, min=0, max=len(note_ids))

    for i, nid in enumerate(note_ids):
        note = mw.col.getNote(nid)
        copy = dict(note)

        if has_any_field(copy, field_groups) and has_field(
            config['fields']['hanzi'], copy
        ):
            d_has_fields += 1

            msg = '''
            <b>Processing:</b> %(hanzi)s<br>
            <b>Filled pinyin:</b> %(pinyin)d notes<br>
            <b>Updated: </b>%(updated)d fields''' % {
                'hanzi': get_hanzi(copy),
                'pinyin': d_added_pinyin,
                'updated': d_updated,
            }
            mw.progress.update(label=msg, value=i)

            hanzi = get_first(config['fields']['hanzi'], copy)
            results = fill_transcript(hanzi, copy)
            results += fill_bopomofo(hanzi, copy)

            if results > 0:
                d_added_pinyin += 1

            fill_all_rubies(hanzi, copy)
            save_note(note, copy)

    mw.progress.finish()
    msg = '''
    <b>Processing:</b> %(hanzi)s<br>
    <b>Filled pinyin:</b> %(pinyin)d notes<br>
    <b>Updated: </b>%(updated)d fields''' % {
        'hanzi': get_hanzi(copy),
        'pinyin': d_added_pinyin,
        'updated': d_updated,
    }
    showInfo(msg)


def bulk_fill_defs():
    prompt = PROMPT_TEMPLATE.format(
        field_names='<i>definition</i> and <i>alternative</i>',
        extra_info='',
    )

    progress_msg_template = '''
            <b>Processing:</b> %(hanzi)s<br>
            <b>Chinese notes:</b> %(has_fields)d<br>
            <b>Translated:</b> %(filled)d<br>
            <b>Failed:</b> %(failed)d'''

    field_groups = ['meaning', 'english', 'german', 'french']

    if not askUser(prompt):
        return

    n_targets = 0
    d_success = 0
    d_failed = 0
    failed_hanzi = []

    note_ids = Finder(mw.col).findNotes('deck:current')
    mw.progress.start(immediate=True, min=0, max=len(note_ids))

    for i, nid in enumerate(note_ids):
        note = mw.col.getNote(nid)
        copy = dict(note)
        hanzi = get_hanzi(copy)

        if has_any_field(copy, field_groups) and hanzi:
            n_targets += 1

            if all_fields_empty(copy, field_groups):
                result = fill_all_defs(hanzi, copy)
                if result:
                    d_success += 1
                else:
                    d_failed += 1
                    if d_failed < 20:
                        failed_hanzi += [hanzi]

            msg = progress_msg_template % {
                'hanzi': hanzi,
                'has_fields': n_targets,
                'filled': d_success,
                'failed': d_failed,
            }
            mw.progress.update(label=msg, value=i)

            save_note(note, copy)

    msg = '''
    <b>Translation complete</b><br>
    <b>Chinese notes:</b> %(has_fields)d<br>
    <b>Translated:</b> %(filled)d<br>
    <b>Failed:</b> %(failed)d''' % {
        'has_fields': n_targets,
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


def bulk_fill_classifiers():
    prompt = PROMPT_TEMPLATE.format(
        field_names='<i>classifier</i>', extra_info=''
    )

    field_groups = ['classifier']

    if not askUser(prompt):
        return

    n_targets = 0
    d_success = 0
    d_failed = 0

    note_ids = Finder(mw.col).findNotes('deck:current')
    mw.progress.start(immediate=True, min=0, max=len(note_ids))

    for i, nid in enumerate(note_ids):
        note = mw.col.getNote(nid)
        copy = dict(note)
        hanzi = get_hanzi(copy)

        if has_any_field(copy, field_groups) and hanzi:
            n_targets += 1

            if all_fields_empty(copy, field_groups):
                if fill_classifier(hanzi, copy):
                    d_success += 1
                else:
                    d_failed += 1

            msg = PROGRESS_TEMPLATE % {
                'hanzi': hanzi,
                'has_fields': n_targets,
                'filled': d_success,
                'failed': d_failed,
            }
            mw.progress.update(label=msg, value=i)

            save_note(note, copy)

    mw.progress.finish()
    showInfo(
        END_TEMPLATE
        % {'has_fields': n_targets, 'filled': d_success, 'failed': d_failed}
    )


def bulk_fill_hanzi():
    prompt = PROMPT_TEMPLATE.format(field_names='<i>hanzi</i>', extra_info='')
    field_groups = ['traditional', 'simplified']

    if not askUser(prompt):
        return

    d_has_fields = 0
    d_success = 0

    note_ids = Finder(mw.col).findNotes('deck:current')
    mw.progress.start(immediate=True, min=0, max=len(note_ids))

    for i, nid in enumerate(note_ids):
        note = mw.col.getNote(nid)
        copy = dict(note)

        if has_any_field(copy, field_groups) and has_field(
            config['fields']['hanzi'], copy
        ):
            d_has_fields += 1

            msg = '''
            <b>Processing:</b> %(hanzi)s<br>
            <b>Updated:</b> %(filled)d''' % {
                'hanzi': get_hanzi(copy),
                'filled': d_success,
            }
            mw.progress.update(label=msg, value=i)

            hanzi = get_first(config['fields']['hanzi'], copy)
            fill_simp(hanzi, copy)
            fill_trad(hanzi, copy)
            fill_color(hanzi, copy)
            d_success = save_note(note, copy)

    msg = '''
    <b>Update complete!</b> %(hanzi)s<br>
    <b>Updated:</b> %(filled)d notes''' % {
        'hanzi': get_hanzi(copy),
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

    d_has_fields = 0
    d_success = 0

    note_ids = Finder(mw.col).findNotes('deck:current')
    mw.progress.start(immediate=True, min=0, max=len(note_ids))

    for i, nid in enumerate(note_ids):
        note = mw.col.getNote(nid)
        copy = dict(note)
        if has_field(config['fields']['silhouette'], copy):
            d_has_fields += 1
            msg = '''
            <b>Processing:</b> %(hanzi)s<br>
            <b>Updated:</b> %(filled)d''' % {
                'hanzi': get_hanzi(copy),
                'filled': d_success,
            }
            mw.progress.update(label=msg, value=i)
            hanzi = get_first(config['fields']['hanzi'], copy)
            fill_silhouette(hanzi, copy)
            d_success = save_note(note, copy)

    msg = '''
    <b>Update complete!</b> %(hanzi)s<br>
    <b>Updated:</b> %(filled)d notes''' % {
        'hanzi': get_hanzi(copy),
        'filled': d_success,
    }
    mw.progress.finish()
    showInfo(msg)
