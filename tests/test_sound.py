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

from unittest.mock import Mock, patch

from . import ChineseTests


class SoundTests(ChineseTests):
    def test_hanzi(self):
        from chinese.sound import sound
        m = Mock(return_value='foo.mp3')
        with patch('chinese.sound.download_sound', m):
            self.assertEqual(
                sound('图书馆', 'Baidu Translate'), '[sound:foo.mp3]')

    def test_non_hanzi(self):
        from chinese.sound import sound
        with patch('chinese.sound.has_hanzi', Mock(return_value=False)):
            self.assertEqual(sound('foo', 'Baidu Translate'), '')


class ExtractSoundTagsTests(ChineseTests):
    def test_extract_sound_tags(self):
        from chinese.sound import extract_sound_tags
        self.assertEqual(
            extract_sound_tags('foo[sound:bar]baz'),
            ('foobaz', '[sound:bar]')
        )


class NoSoundTests(ChineseTests):
    def test_no_sound(self):
        from chinese.sound import no_sound
        self.assertEqual(no_sound('a [sound:] b'), 'a  b')
