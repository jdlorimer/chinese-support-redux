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

from unittest.mock import Mock, patch

from chinese.sound import extract_tags, no_sound, sound
from tests import Base


class Download(Base):
    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            sound('图书馆[foo bar baz]', 'foo|bar')


class Sound(Base):
    def setUp(self):
        super().setUp()
        self.patcher = patch('chinese.sound.AudioDownloader', Mock())
        self.mock = self.patcher.start()

    def tearDown(self):
        super().tearDown()
        self.patcher.stop()

    def test_hanzi(self):
        mock = Mock()
        mock.download = Mock(return_value='foo.mp3')
        self.mock.return_value = mock
        self.assertEqual(sound('图书馆', 'baidu|zh'), '[sound:foo.mp3]')

    def test_no_hanzi(self):
        with patch('chinese.sound.has_hanzi', Mock(return_value=False)):
            self.assertEqual(sound('foo', 'baidu|zh'), '')

    def test_ruby(self):
        sound('图书馆[foo bar baz]', 'baidu|zh')
        self.mock.assert_called_once_with('图书馆', 'baidu|zh')

    def test_bogus_source(self):
        with self.assertRaises(ValueError):
            sound('图书馆[foo bar baz]', 'foobar')


class ExtractSoundTags(Base):
    def test_single_tag(self):
        self.assertEqual(
            extract_tags('foo[sound:bar]'), ('foo', '[sound:bar]')
        )

    def test_multiple_tags(self):
        self.assertEqual(
            extract_tags('foo[sound:bar]baz[sound:qux]'),
            ('foobaz', '[sound:bar][sound:qux]'),
        )

    def test_no_tags(self):
        self.assertEqual(extract_tags('foo'), ('foo', ''))

    def test_empty_tag(self):
        self.assertEqual(extract_tags('foo[sound:]'), ('foo', '[sound:]'))


class NoSound(Base):
    def test_single_tag(self):
        self.assertEqual(no_sound('foo[sound:bar]'), 'foo')

    def test_multiple_tags(self):
        self.assertEqual(no_sound('foo[sound:bar]baz[sound:qux]'), 'foobaz')

    def test_no_tags(self):
        self.assertEqual(no_sound('foo'), 'foo')

    def test_empty_tag(self):
        self.assertEqual(no_sound('foo[sound:]'), 'foo')
