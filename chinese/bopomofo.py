# Copyright © 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2014 Alex Griffin <alex@alexjgriffin.com>
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

from .consts import bopomofo_replacements
from .util import cleanup


def bopomofo(pinyin):
    assert isinstance(pinyin, list)
    result = []
    for word in pinyin:
        s = cleanup(word).lower()
        for (a, b) in bopomofo_replacements:
            s = s.replace(a, b)
        result.append(s)
    return result
