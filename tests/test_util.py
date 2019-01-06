# Copyright © 2018-2019 Joseph Lorimer <luoliyan@posteo.net>
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

from chinese.util import align, cleanup, get_first, hide, no_hidden, set_all
from tests import ChineseTest


class Util(ChineseTest):
    def test_hide(self):
        self.assertEqual(hide('foo', 'bar'), 'foo <!-- bar -->')

    def test_no_hidden(self):
        self.assertEqual(no_hidden('foo <!-- bar --> baz'), 'foo baz')
        self.assertEqual(no_hidden('foo<!--bar-->baz'), 'foo baz')

    def test_set_all(self):
        d = {'foo': '', 'bar': '', 'baz': ''}
        set_all(['foo', 'baz'], d, 'qux')
        self.assertEqual(d, {'foo': 'qux', 'bar': '', 'baz': 'qux'})


class Cleanup(ChineseTest):
    def test_cloze(self):
        self.assertEqual(cleanup('{{c1::foo::bar}}'), 'foo')


class GetAny(ChineseTest):
    def test_content(self):
        self.assertEqual(get_first(['foo'], {'foo': 'bar'}), 'bar')

    def test_no_content(self):
        self.assertEqual(get_first(['foo'], {'foo': ''}), '')

    def test_no_field(self):
        self.assertEqual(get_first(['foo'], {'bar': 'baz'}), '')

    def test_multiple_fields(self):
        note = {'foo': 'bar', 'baz': 'qux'}
        self.assertEqual(get_first(['foo', 'baz'], note), 'bar')
        self.assertEqual(get_first(['baz', 'foo'], note), 'qux')


class Align(ChineseTest):
    def test_align(self):
        self.assertEqual(
            align(['(', '我', ')'], ['wǒ']),
            [('(', None), ('我', 'wǒ'), (')', None)],
        )

    def test_empty(self):
        self.assertEqual(align([], []), [])
        self.assertEqual(align(['我'], []), [('我', None)])
        self.assertEqual(align([], ['我']), [(None, '我')])
