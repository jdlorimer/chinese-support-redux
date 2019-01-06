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

from chinese.ruby import ruby, ruby_bottom, ruby_top, separate_ruby
from tests import ChineseTest


class Ruby(ChineseTest):
    def test_char(self):
        self.assertEqual(ruby(['你'], 'Pinyin'), ['你[nǐ]'])

    def test_word(self):
        self.assertEqual(ruby(['图书馆'], 'Pinyin'), ['图[tú]书[shū]馆[guǎn]'])

    def test_chars(self):
        self.assertEqual(
            ruby(['图', '书', '馆'], 'Pinyin'), ['图[tú]', '书[shū]', '馆[guǎn]']
        )

    def test_ruby_top(self):
        self.assertEqual(ruby_top('汉[hàn]字[zì]'), 'hàn zì')
        self.assertEqual(ruby_top('hànzì'), 'hànzì')
        self.assertEqual(ruby_top('汉字'), '')

    def test_ruby_bottom(self):
        self.assertEqual(ruby_bottom('汉[hàn]字[zì]'), '汉 字')
        self.assertEqual(ruby_bottom('汉字'), '汉字')
        self.assertEqual(ruby_bottom('hànzì'), '')

    def test_bopomofo(self):
        self.assertEqual(ruby(['機場'], 'Bopomofo'), ['機[ㄐㄧ]場[ㄔㄤˇ]'])
        self.assertEqual(ruby(['機', '場'], 'Bopomofo'), ['機[ㄐㄧ]', '場[ㄔㄤˊ]'])

    def test_bopomofo_punc(self):
        self.assertEqual(ruby(['機場。'], 'Bopomofo'), ['機[ㄐㄧ]場[ㄔㄤˇ]。'])
        self.assertEqual(
            ruby(['機', '場', '。'], 'Bopomofo'), ['機[ㄐㄧ]', '場[ㄔㄤˊ]', '。']
        )


class SeparateRuby(ChineseTest):
    def test_one_word(self):
        self.assertEqual(
            separate_ruby(['图[tú]书[shū]馆[guǎn]']), [('图书馆', 'túshūguǎn')]
        )

    def test_multiple_words(self):
        self.assertEqual(
            separate_ruby(['图[tú]', '书[shū]', '馆[guǎn]']),
            [('图', 'tú'), ('书', 'shū'), ('馆', 'guǎn')],
        )

    def test_no_ruby(self):
        self.assertEqual(
            separate_ruby(['tú', 'shū', 'guǎn']),
            [('', 'tú'), ('', 'shū'), ('', 'guǎn')],
        )
