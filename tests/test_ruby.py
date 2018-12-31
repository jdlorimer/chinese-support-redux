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

from chinese.ruby import ruby, ruby_bottom, ruby_top
from tests import ChineseTest


class Ruby(ChineseTest):
    def test_single_char(self):
        self.assertEqual(ruby('你', 'Pinyin'), ['你[nǐ]'])

    def test_multiple_chars(self):
        self.assertEqual(ruby('图书馆', 'Pinyin'), ['图[tú]', '书[shū]', '馆[guǎn]'])

    def test_ruby_top(self):
        self.assertEqual(ruby_top('汉[hàn]字[zì]'), 'hàn zì')

    def test_ruby_bottom(self):
        self.assertEqual(ruby_bottom('汉[hàn]字[zì]'), '汉 字')
