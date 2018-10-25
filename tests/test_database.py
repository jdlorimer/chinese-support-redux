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

from unittest import skipIf, skip
from unittest.mock import MagicMock, Mock, patch

from . import ChineseTests, NO_INTEGRATION


class DictionaryTests(ChineseTests):
    def setUp(self):
        super().setUp()
        from chinese.database import DictDB
        with patch('chinese.database.connect', MagicMock()):
            self.db = DictDB()

    def test_no_word(self):
        self.assertEqual(self.db.get_classifiers(''), [])

    def test_no_classifier(self):
        self.db.c.fetchall = Mock(return_value=[])
        self.assertEqual(self.db.get_classifiers('foo'), [])

    def test_multiple_classifiers(self):
        self.db.c.fetchall = Mock(return_value=[('bar',), ('baz',)])
        self.assertEqual(self.db.get_classifiers('foo'), ['bar', 'baz'])


@skipIf(NO_INTEGRATION, 'integration tests disabled')
class DictionaryIntegrationTests(ChineseTests):
    def test_get_classifiers(self):
        from chinese.database import DictDB
        db = DictDB()
        self.assertEqual(db.get_classifiers('猫'), ['隻|只[zhi1]'])
        self.assertEqual(db.get_classifiers('签证'), ['個|个[ge4]'])
        self.assertEqual(
            db.get_classifiers('筷子'),
            ['對|对[dui4]', '根[gen1]', '把[ba3]', '雙|双[shuang1]']
        )
