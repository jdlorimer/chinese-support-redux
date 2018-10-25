# Copyright © 2018 Joseph Lorimer <luoliyan@posteo.net>
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

from . import ChineseTests


class HasHanziTests(ChineseTests):
    def setUp(self):
        super().setUp()
        from chinese.hanzi import has_hanzi
        self.func = has_hanzi

    def test_all_hanzi(self):
        self.assertTrue(self.func('现在'))

    def test_no_hanzi(self):
        self.assertFalse(self.func('now'))

    def test_mixed(self):
        self.assertTrue(self.func('现在now'))


class SimplifyTests(ChineseTests):
    def test_simplify(self):
        from chinese.hanzi import simplify
        self.dictionary.get_simplified = Mock(return_value='simp')
        self.assertEqual(simplify('繁體字'), 'simp')


class TraditionalTests(ChineseTests):
    def test_traditional(self):
        from chinese.hanzi import traditional
        self.dictionary.get_traditional = Mock(return_value='trad')
        self.assertEqual(traditional('簡體字'), 'trad')
