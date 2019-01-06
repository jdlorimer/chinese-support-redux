# Copyright © 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2019 Joseph Lorimer <luoliyan@posteo.net>
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

from re import findall, sub

from .consts import sound_tag_regex
from .hanzi import has_hanzi
from .main import config
from .tts import download_sound
from .util import cleanup


def sound(hanzi, source=None):
    """Returns sound tag for a given Hanzi string."""

    from .ruby import ruby_bottom, has_ruby

    if not has_hanzi(hanzi):
        return ''

    if not source:
        source = config['speech']

    if has_ruby(hanzi):
        hanzi = ruby_bottom(hanzi)

    if not hanzi:
        return ''

    options = {
        'Google Mandarin (PRC)': ('google', 'zh-cn'),
        'Google Mandarin (Taiwan)': ('google', 'zh-tw'),
        'Baidu Translate': ('baidu', 'zh'),
    }

    if source in options:
        return '[sound:%s]' % download_sound(hanzi, options[source])

    return ''


def extract_sound_tags(text):
    tags = findall(sound_tag_regex, text)
    if not tags:
        return text, ''
    return no_sound(text), ''.join(tags)


def no_sound(text):
    return sub(sound_tag_regex, '', text)
