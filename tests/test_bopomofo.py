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

from unittest import skip

from . import ChineseTests


class BopomofoTests(ChineseTests):
    def setUp(self):
        super().setUp()
        from chinese.bopomofo import bopomofo
        self.func = bopomofo

    def test_pinyin_no_tone(self):
        self.assertEqual(self.func('zhu yin'), 'ㄓㄨ ㄧㄣ')

    def test_pinyin_tone_number(self):
        self.assertEqual(self.func('zhu4 yin1'), 'ㄓㄨˋ ㄧㄣ')

    @skip
    def test_pinyin_tone_mark(self):
        self.assertEqual(self.func('zhù yīn'), '')

    @skip
    def test_joined_word(self):
        self.assertEqual(self.func('zhùyīn'), '')

    @skip
    def test_hanzi(self):
        self.assertEqual(self.func('注音'), '')
