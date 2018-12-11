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

from unittest.mock import patch

from chinese.behavior import fill_all_definitions, update_Pinyin_fields
from tests import ChineseTests


class FillAllDefinitionsTests(ChineseTests):
    config = {
        'dictionary': 'en',
        'fields': {
            'meaning': ['Meaning'],
            'english': ['English'],
            'german': ['German'],
            'french': ['French'],
            'classifier': ['Classifier'],
        },
    }

    def test_no_classifier_field(self):
        with patch('chinese.behavior.config', self.config):
            hanzi = '图书馆'
            note = {
                'Meaning': '',
                'English': '',
                'German': '',
                'French': '',
            }
            classifier = (
                '<span class="tone1"><ruby>家<rt>jiā</rt></ruby></span>, '
                '<span class="tone4"><ruby>個<rt>gè</rt></ruby></span>|'
                '<span class="tone4">个</span>'
            )
            english = ' \tlibrary\n<br><br>Cl: ' + classifier
            german = ' \tBibliothek (S, Lit\n<br><br>Cl: ' + classifier
            french = ' \tbibliothèque\n<br><br>Cl: ' + classifier
            self.assertEqual(fill_all_definitions(hanzi, note), 4)
            self.assertEqual(note['Meaning'], english)
            self.assertEqual(note['English'], english)
            self.assertEqual(note['German'], german)
            self.assertEqual(note['French'], french)

    def test_classifier_field(self):
        with patch('chinese.behavior.config', self.config):
            hanzi = '图书馆'
            note = {
                'Meaning': '',
                'Classifier': '',
            }
            classifier = (
                '<span class="tone1"><ruby>家<rt>jiā</rt></ruby></span>, '
                '<span class="tone4"><ruby>個<rt>gè</rt></ruby></span>|'
                '<span class="tone4">个</span>'
            )
            self.assertEqual(fill_all_definitions(hanzi, note), 1)
            self.assertEqual(note['Meaning'], ' \tlibrary\n<br>')
            self.assertEqual(note['Classifier'], classifier)

class UpdatePinyinFieldsTest(ChineseTests):
    config = {
        'dictionary': 'en',
        'fields': {
            'pinyin': ["Pinyin"]
        }
    }

    def test_twocharacterword(self):
        with patch('chinese.behavior.config', self.config):
            hanzi = '中国'
            note = {
                'Pinyin': '',
            }
            # mind the spaces here
            # if there are spaces between the spans and zhongguo in the comment,
            # then transcribe was treating 中 and 国 as two separate words, what we do not want
            pinyin = (
                '<span class="tone1">zhōng</span><span class="tone2">guó</span><!--zhongguo-->'
            )
            self.assertEqual(update_Pinyin_fields(hanzi, note), 1)
            self.assertEqual(note['Pinyin'], pinyin)