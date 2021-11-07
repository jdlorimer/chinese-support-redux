# Copyright © 2013 Chris Hatch <foonugget@gmail.com>
# Copyright © 2014 Thomas Tempe <thomas.tempe@alysse.org>
# Copyright © 2019 Daniel Rich <https://github.com/danielrich>
# Copyright © 2017-2020 Joseph Lorimer <joseph@lorimer.me>
# Copyright © 2020 Joe Minicucci <https://joeminicucci.com>
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
from aqt.utils import askUser, showInfo, showText

from .behavior import (
    fill_all_defs,
    fill_all_rubies,
    fill_classifier,
    fill_color,
    fill_frequency,
    fill_silhouette,
    fill_simp,
    fill_sound,
    fill_trad,
    fill_transcript,
    fill_usage,
    update_fields,
)
from .hanzi import get_hanzi
from .main import config
from .util import (
    all_fields_empty,
    get_first,
    has_any_field,
    save_note,
)

PROMPT_TEMPLATE = (
    '<div>This will update the {field_names} fields in the current deck.</div>'
    '<div>Please back up your Anki collection first!</div>'
    '{extra_info}'
    '<div><b>Continue?</b></div>'
)

PROGRESS_TEMPLATE = (
    '<b>Hanzi:</b> %(hanzi)s<br>'
    '<b>Notes Processed:</b> %(n_processed)d<br>'
    '<b>Fields Updated:</b> %(n_updated)d<br>'
    '<b>Failed Field Updates:</b> %(n_failed)d'
)

END_TEMPLATE = (
    '<b>Bulk filling complete</b><br>'
    '<b>Processed:</b> %(has_fields)d<br>'
    '<b>Updated:</b> %(filled)d<br>'
    '<b>Failed:</b> %(failed)d'
)


def bulk_fill_all():
    prompt = (
        '<div>This will update <i>all</i> non-audio fields in the current deck.</div>'
        '<div>Please back up your Anki collection first!</div>'
        '<div><b>Continue?</b></div>'
    )

    if not askUser(prompt):
        return

    note_ids = Finder(mw.col).findNotes('deck:current')
    mw.progress.start(immediate=True, min=0, max=len(note_ids))
    n_updated = 0
    n_failed = 0  # FIXME
    exclude = config.get_fields(['sound', 'mandarinSound', 'cantoneseSound'])

    for i, nid in enumerate(note_ids):
        note = mw.col.getNote(nid)
        fields = [
            f
            for f in mw.col.models.fieldNames(note.model())
            if f not in exclude
        ]
        n_updated += update_fields(note, 'Hanzi', fields)
        msg = PROGRESS_TEMPLATE % {
            'hanzi': get_hanzi(dict(note)),
            'n_processed': i,
            'n_updated': n_updated,
            'n_failed': n_failed,
        }

        mw.progress.update(label=msg, value=i)
        note.flush()

    mw.progress.finish()
    showInfo(
        '<b>Bulk filling complete</b><br>'
        '<b>Processed:</b> {}<br>'.format(len(note_ids))
    )


def bulk_fill_sound():
    prompt = PROMPT_TEMPLATE.format(
        field_names='<i>Sound</i>',
        extra_info=(
            '<div>There will be a 5 second delay between each sound request,'
            ' so this may take a while.</div>'
        ),
    )

    fields = config.get_fields(['sound', 'mandarinSound', 'cantoneseSound'])

    if not askUser(prompt):
        return

    d_has_fields = 0
    d_already_had_sound = 0
    n_updated = 0
    n_failed = 0

    note_ids = Finder(mw.col).findNotes('deck:current')
    mw.progress.start(immediate=True, min=0, max=len(note_ids))

    for i, nid in enumerate(note_ids):
        orig = mw.col.getNote(nid)
        copy = dict(orig)

        if has_any_field(copy, fields) and has_any_field(
            config['fields']['hanzi'], copy
        ):
            d_has_fields += 1
            hanzi = get_first(config['fields']['hanzi'], copy)

            if all_fields_empty(copy, fields):
                msg = '''
                <b>Processing:</b> %(hanzi)s<br>
                <b>Updated:</b> %(n_updated)d notes<br>
                <b>Failed:</b> %(n_failed)d notes''' % {
                    'hanzi': get_hanzi(copy),
                    'n_updated': n_updated,
                    'n_failed': n_failed,
                }
                mw.progress.update(label=msg, value=i)
                s, f = fill_sound(hanzi, copy)
                n_updated += s
                n_failed += f
                save_note(orig, copy)
                sleep(5)
            else:
                d_already_had_sound += 1

    mw.progress.finish()
    msg = '''
%(n_updated)d new pronunciations downloaded

%(n_failed)d downloads failed

%(have)d/%(d_has_fields)d notes now have pronunciation''' % {
        'n_updated': n_updated,
        'n_failed': n_failed,
        'have': d_already_had_sound + n_updated,
        'd_has_fields': d_has_fields,
    }
    if n_failed > 0:
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

    fields = config.get_fields(
        ['pinyin', 'pinyinTaiwan', 'cantonese', 'bopomofo']
    )

    if not askUser(prompt):
        return

    d_has_fields = 0
    d_added_pinyin = 0
    n_updated = 0

    note_ids = Finder(mw.col).findNotes('deck:current')
    mw.progress.start(immediate=True, min=0, max=len(note_ids))

    for i, nid in enumerate(note_ids):
        note = mw.col.getNote(nid)
        copy = dict(note)

        if has_any_field(copy, fields) and has_any_field(
            config['fields']['hanzi'], copy
        ):
            d_has_fields += 1

            msg = '''
            <b>Processing:</b> %(hanzi)s<br>
            <b>Filled pinyin:</b> %(pinyin)d notes<br>
            <b>Updated: </b>%(updated)d fields''' % {
                'hanzi': get_hanzi(copy),
                'pinyin': d_added_pinyin,
                'updated': n_updated,
            }
            mw.progress.update(label=msg, value=i)

            hanzi = get_first(config['fields']['hanzi'], copy)
            results = fill_transcript(hanzi, copy)

            if results > 0:
                d_added_pinyin += 1

            fill_all_rubies(hanzi, copy)
            save_note(note, copy)

    mw.progress.finish()
    msg = '''
    <b>Processed:</b> %(hanzi)s<br>
    <b>Filled pinyin:</b> %(pinyin)d notes<br>
    <b>Updated: </b>%(updated)d fields''' % {
        'hanzi': get_hanzi(copy),
        'pinyin': d_added_pinyin,
        'updated': n_updated,
    }
    showInfo(msg)


def bulk_fill_defs():
    prompt = PROMPT_TEMPLATE.format(
        field_names='<i>definition</i> and <i>alternative</i>', extra_info=''
    )

    progress_msg_template = '''
            <b>Processing:</b> %(hanzi)s<br>
            <b>Chinese notes:</b> %(has_fields)d<br>
            <b>Translated:</b> %(filled)d<br>
            <b>Failed:</b> %(failed)d'''

    fields = config.get_fields(['english', 'german', 'french'])

    if not askUser(prompt):
        return

    n_processed = 0
    n_updated = 0
    n_failed = 0
    n_notfilled = 0
    failed_hanzi = []

    note_ids = Finder(mw.col).findNotes('deck:current')
    mw.progress.start(immediate=True, min=0, max=len(note_ids))

    for i, note_id in enumerate(note_ids):
        note = mw.col.getNote(note_id)
        copy = dict(note)
        hanzi = get_hanzi(copy)

        if has_any_field(copy, fields) and hanzi:
            n_processed += 1

            try:
                if all_fields_empty(copy, fields):
                    result = fill_all_defs(hanzi, copy)
                    if result:
                        n_updated += 1
                    else:
                        n_notfilled += 1
            except:
                n_failed += 1
                failed_hanzi += [hanzi]

            msg = progress_msg_template % {
                'hanzi': hanzi,
                'has_fields': n_processed,
                'filled': n_updated,
                'failed': n_failed,
            }
            mw.progress.update(label=msg, value=i)

            save_note(note, copy)

    msg = '''
    <b>Translation complete</b><br>
    <b>Chinese notes:</b> %(has_fields)d<br>
    <b>Translated:</b> %(filled)d<br>
    <b>Failed:</b> %(failed)d''' % {
        'has_fields': n_processed,
        'filled': n_updated,
        'failed': n_failed,
    }
    if n_failed > 0:
        failed_msg = (
            'Translation failures may come either from connection issues '
            "(if you're using an online translation service), or because some "
            'words are not it the dictionary (for local dictionaries).\n'
            'The following notes failed: \n\n'
            + ', '.join(failed_hanzi)
        )
        showText(failed_msg, copyBtn=True)
    mw.progress.finish()
    showInfo(msg)


def bulk_fill_classifiers():
    prompt = PROMPT_TEMPLATE.format(
        field_names='<i>classifier</i>', extra_info=''
    )

    fields = config.get_fields(['classifier'])

    if not askUser(prompt):
        return

    n_processed = 0
    n_updated = 0
    n_failed = 0

    note_ids = Finder(mw.col).findNotes('deck:current')
    mw.progress.start(immediate=True, min=0, max=len(note_ids))

    for i, nid in enumerate(note_ids):
        note = mw.col.getNote(nid)
        copy = dict(note)
        hanzi = get_hanzi(copy)

        if has_any_field(copy, fields) and hanzi:
            n_processed += 1

            if all_fields_empty(copy, fields):
                if fill_classifier(hanzi, copy):
                    n_updated += 1
                else:
                    n_failed += 1

            msg = PROGRESS_TEMPLATE % {
                'hanzi': hanzi,
                'n_processed': n_processed,
                'n_updated': n_updated,
                'n_failed': n_failed,
            }
            mw.progress.update(label=msg, value=i)

            save_note(note, copy)

    mw.progress.finish()
    showInfo(
        END_TEMPLATE
        % {'has_fields': n_processed, 'filled': n_updated, 'failed': n_failed}
    )


def bulk_fill_hanzi():
    prompt = PROMPT_TEMPLATE.format(field_names='<i>hanzi</i>', extra_info='')

    fields = config.get_fields(['traditional', 'simplified'])

    if not askUser(prompt):
        return

    d_has_fields = 0
    n_updated = 0

    note_ids = Finder(mw.col).findNotes('deck:current')
    mw.progress.start(immediate=True, min=0, max=len(note_ids))

    for i, nid in enumerate(note_ids):
        note = mw.col.getNote(nid)
        copy = dict(note)

        if has_any_field(copy, fields) and has_any_field(
            config['fields']['hanzi'], copy
        ):
            d_has_fields += 1

            msg = '''
            <b>Processing:</b> %(hanzi)s<br>
            <b>Updated:</b> %(filled)d''' % {
                'hanzi': get_hanzi(copy),
                'filled': n_updated,
            }
            mw.progress.update(label=msg, value=i)

            hanzi = get_first(config['fields']['hanzi'], copy)
            fill_simp(hanzi, copy)
            fill_trad(hanzi, copy)
            fill_color(hanzi, copy)
            n_updated = save_note(note, copy)

    msg = '''
    <b>Update complete!</b> %(hanzi)s<br>
    <b>Updated:</b> %(filled)d notes''' % {
        'hanzi': get_hanzi(copy),
        'filled': n_updated,
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
    n_updated = 0

    note_ids = Finder(mw.col).findNotes('deck:current')
    mw.progress.start(immediate=True, min=0, max=len(note_ids))

    for i, nid in enumerate(note_ids):
        note = mw.col.getNote(nid)
        copy = dict(note)
        if has_any_field(config['fields']['silhouette'], copy):
            d_has_fields += 1
            msg = '''
            <b>Processing:</b> %(hanzi)s<br>
            <b>Updated:</b> %(filled)d''' % {
                'hanzi': get_hanzi(copy),
                'filled': n_updated,
            }
            mw.progress.update(label=msg, value=i)
            hanzi = get_first(config['fields']['hanzi'], copy)
            fill_silhouette(hanzi, copy)
            n_updated = save_note(note, copy)

    msg = '''
    <b>Update complete!</b> %(hanzi)s<br>
    <b>Updated:</b> %(filled)d notes''' % {
        'hanzi': get_hanzi(copy),
        'filled': n_updated,
    }
    mw.progress.finish()
    showInfo(msg)


def bulk_fill_usage():
    prompt = PROMPT_TEMPLATE.format(
        field_names='<i>usage</i>', extra_info=''
    )

    progress_msg_template = '''
            <b>Processing:</b> %(hanzi)s<br>
            <b>Chinese notes:</b> %(has_fields)d<br>
            <b>Cards with Sentences added:</b> %(filled)d<br>
            <b>Cards with no Sentences added:</b> %(not_filled)d<br>
            <b>Failed:</b> %(failed)d'''

    fields = config.get_fields(['usage'])

    if not askUser(prompt):
        return

    n_processed = 0
    n_updated = 0
    n_failed = 0
    n_notfilled = 0
    failed_hanzi = []

    note_ids = Finder(mw.col).findNotes('deck:current')
    mw.progress.start(immediate=True, min=0, max=len(note_ids))

    for i, note_id in enumerate(note_ids):
        note = mw.col.getNote(note_id)
        copy = dict(note)
        hanzi = get_hanzi(copy)

        if has_any_field(copy, fields) and hanzi:
            n_processed += 1

            try:
                if all_fields_empty(copy, fields):
                    result = fill_usage(hanzi, copy)
                    if result:
                        n_updated += 1
                    else:
                        n_notfilled += 1
            except:
                n_failed += 1
                failed_hanzi.append(hanzi)

            msg = progress_msg_template % {
                'hanzi': hanzi,
                'has_fields': n_processed,
                'filled': n_updated,
                'not_filled': n_notfilled,
                'failed': n_failed,
            }
            mw.progress.update(label=msg, value=i)

            save_note(note, copy)

    msg = '''
    <b>Usage Additions Complete</b><br>
    <b>Chinese Notes:</b> %(has_fields)d<br>
    <b>Usage Fields Filled:</b> %(filled)d<br>
    <b>Usage Fields Not Filled:</b> %(not_filled)d<br>
    <b>Failed:</b> %(failed)d''' % {
        'has_fields': n_processed,
        'filled': n_updated,
        'not_filled': n_notfilled,
        'failed': n_failed,
    }
    if n_failed > 0:
        failed_msg = (
            'Usages may not be available in the database\'s data set. '
            'Custom data can be added to the english_usage column in the'
            'chinese.db database.\n'
            'The following notes failed: \n\n'
            + ', '.join(failed_hanzi)
        )
        showText(failed_msg, copyBtn=True)
    mw.progress.finish()
    showInfo(msg)


def bulk_fill_frequency():
    prompt = PROMPT_TEMPLATE.format(field_names="<i>frequency</i>", extra_info="")

    progress_msg_template = """
            <b>Processing:</b> %(hanzi)s<br>
            <b>Chinese notes:</b> %(has_fields)d<br>
            <b>Cards with Frequency added:</b> %(filled)d<br>
            <b>Cards with no Frequency added:</b> %(not_filled)d<br>
            <b>Failed:</b> %(failed)d"""

    target_fields = config.get_fields(["frequency"])
    hanzi_fields = config.get_fields(["hanzi"])

    if not askUser(prompt):
        return

    n_processed = 0
    n_updated = 0
    n_failed = 0
    n_notfilled = 0
    failed_hanzi = []

    note_ids = mw.col.findNotes("deck:current")
    mw.progress.start(immediate=True, min=0, max=len(note_ids))

    for i, note_id in enumerate(note_ids):
        note = mw.col.getNote(note_id)
        copy = dict(note)

        # Ensure note type has hanzi present
        hanzi = None
        if has_any_field(copy, hanzi_fields):
            hanzi = get_hanzi(copy)

        if has_any_field(copy, target_fields) and hanzi:
            n_processed += 1

            try:
                if all_fields_empty(copy, target_fields):
                    filled = fill_frequency(hanzi, copy)
                    if filled:
                        n_updated += 1
                    else:
                        n_notfilled += 1
            except:
                n_failed += 1
                failed_hanzi.append(hanzi)

            msg = progress_msg_template % {
                "hanzi": hanzi,
                "has_fields": n_processed,
                "filled": n_updated,
                "not_filled": n_notfilled,
                "failed": n_failed,
            }
            mw.progress.update(label=msg, value=i)

            save_note(note, copy)

    msg = """
    <b>Frequency Additions Complete</b><br>
    <b>Chinese Notes:</b> %(has_fields)d<br>
    <b>Frequency Fields Filled:</b> %(filled)d<br>
    <b>Frequency Fields Not Filled:</b> %(not_filled)d<br>
    <b>Failed:</b> %(failed)d""" % {
        "has_fields": n_processed,
        "filled": n_updated,
        "not_filled": n_notfilled,
        "failed": n_failed,
    }
    if n_failed > 0:
        failed_msg = (
            "Frequency may not be available in the database's data set. "
            "Custom data can be added to the data/freq/internet-zh file."
            "The following notes failed: \n\n" + ", ".join(failed_hanzi)
        )
        showText(failed_msg, copyBtn=True)
    mw.progress.finish()
    showInfo(msg)
