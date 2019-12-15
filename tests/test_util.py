# Copyright © 2018-2019 Joseph Lorimer <joseph@lorimer.me>
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

from unittest.mock import Mock

from chinese.util import (
    align,
    cleanup,
    get_first,
    has_field,
    has_any_field,
    hide,
    no_hidden,
    save_note,
    set_all,
)
from tests import Base


class Util(Base):
    def test_hide(self):
        self.assertEqual(hide('foo', 'bar'), 'foo <!-- bar -->')

    def test_no_hidden(self):
        self.assertEqual(no_hidden('foo <!-- bar --> baz'), 'foo baz')
        self.assertEqual(no_hidden('foo<!--bar-->baz'), 'foo baz')

    def test_set_all(self):
        d = {'foo': '', 'bar': '', 'baz': ''}
        set_all(['foo', 'baz'], d, 'qux')
        self.assertEqual(d, {'foo': 'qux', 'bar': '', 'baz': 'qux'})


class Cleanup(Base):
    def test_cloze(self):
        self.assertEqual(cleanup('{{c1::foo::bar}}'), 'foo')

    def test_whitespace(self):
        self.assertEqual(cleanup(' \t '), '')

    def test_empty_string(self):
        self.assertEqual(cleanup(''), '')

    def test_none(self):
        with self.assertRaises(ValueError):
            cleanup(None)


class HasField(Base):
    def test_field_present(self):
        self.assertEqual(has_field('foo', {'foo': ''}), True)

    def test_field_missing(self):
        self.assertEqual(has_field('foo', {'bar': ''}), False)

class HasAnyField(Base):
    def test_field_present(self):
        self.assertEqual(has_any_field({'bar': ''}, ['foo', 'bar']), True)

    def test_field_missing(self):
        self.assertEqual(has_any_field({'baz': ''}, ['foo', 'bar']), False)


class GetFirst(Base):
    def test_field_with_text(self):
        self.assertEqual(get_first(['foo'], {'foo': 'bar'}), 'bar')

    def test_empty_field(self):
        self.assertEqual(get_first(['foo'], {'foo': ''}), '')

    def test_no_field(self):
        self.assertEqual(get_first(['foo'], {'bar': 'baz'}), None)

    def test_multiple_fields(self):
        note = {'foo': 'bar', 'baz': 'qux'}
        self.assertEqual(get_first(['foo', 'baz'], note), 'bar')
        self.assertEqual(get_first(['baz', 'foo'], note), 'qux')


class Align(Base):
    def test_align(self):
        self.assertEqual(
            align(['(', '我', ')'], ['wǒ']),
            [('(', None), ('我', 'wǒ'), (')', None)],
        )

    def test_empty(self):
        self.assertEqual(align([], []), [])
        self.assertEqual(align(['我'], []), [('我', None)])
        self.assertEqual(align([], ['我']), [(None, '我')])

    def test_mixed_english_chinese(self):
        self.assertEqual(
            align(['Brian', '的'], ['Brian', 'de']),
            [('Brian', 'Brian'), ('的', 'de')],
        )


class SaveNote(Base):
    def test_save_note(self):
        class Note(dict):
            flush = Mock()

        note = Note()
        note.update({'hanzi': '我', 'pinyin': ''})
        copy = {'hanzi': '我', 'pinyin': 'wǒ'}
        self.assertEqual(save_note(note, copy), 1)
        self.assertEqual(note['pinyin'], 'wǒ')
        note.flush.assert_called_once()
