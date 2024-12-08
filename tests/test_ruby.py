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

from chinese.ruby import ruby, ruby_bottom, ruby_top, separate_ruby
from tests import Base


class Ruby(Base):
    def test_char(self):
        self.assertEqual(ruby(['你'], 'pinyin'), ['你[nǐ]'])

    def test_word(self):
        self.assertEqual(ruby(['图书馆'], 'pinyin'), ['图[tú]书[shū]馆[guǎn]'])

    def test_chars(self):
        self.assertEqual(
            ruby(['图', '书', '馆'], 'pinyin'), ['图[tú]', '书[shū]', '馆[guǎn]']
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
        self.assertEqual(ruby(['機場'], 'bopomofo'), ['機[ㄐㄧ]場[ㄔㄤˇ]'])
        self.assertEqual(ruby(['機', '場'], 'bopomofo'), ['機[ㄐㄧ]', '場[ㄔㄤˇ]'])
        self.assertEqual(
            ruby(['加拿大人'], 'bopomofo'), ['加[ㄐㄧㄚ]拿[ㄋㄚˊ]大[ㄉㄚˋ]人[ㄖㄣˊ]']
        )

    def test_bopomofo_punc(self):
        self.assertEqual(ruby(['機場。'], 'bopomofo'), ['機[ㄐㄧ]場[ㄔㄤˇ]。'])
        self.assertEqual(
            ruby(['機', '場', '。'], 'bopomofo'), ['機[ㄐㄧ]', '場[ㄔㄤˇ]', '。']
        )

    def test_jyutping_available(self):
        self.assertEqual(ruby(['中學'], 'jyutping'), ['中[zung1]學[hok6]'])

    def test_jyutping_not_available(self):
        self.assertEqual(ruby(['欣然'], 'jyutping'), ['欣然'])


class SeparateRuby(Base):
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
