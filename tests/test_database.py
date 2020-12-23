# Copyright © 2018-2019 Joseph Lorimer <joseph@lorimer.me>
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

from chinese.database import Dictionary as D
from tests import Base


class Dictionary(Base):
    def test_no_word(self):
        self.assertEqual(D().get_classifiers(''), [])

    def test_no_classifier(self):
        self.assertEqual(D().get_classifiers('foo'), [])

    def test_single_classifier(self):
        self.assertEqual(D().get_classifiers('猫'), ['隻|只[zhi1]'])
        self.assertEqual(D().get_classifiers('签证'), ['個|个[ge4]'])

    def test_multiple_classifiers(self):
        self.assertEqual(
            D().get_classifiers('筷子'),
            ['對|对[dui4]', '根[gen1]', '把[ba3]', '雙|双[shuang1]'],
        )

    def test_variants(self):
        self.assertEqual(D().get_variants('陵夷'), ['凌夷'])

    def test_jyutping(self):
        self.assertEqual(D().get_cantonese('上海人', 'trad'), 'soeng6 hoi2 jan4')
