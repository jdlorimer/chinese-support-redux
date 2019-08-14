# Copyright © 2013 Ernest French <ernestfrench@gmail.com>
# Copyright © 2019 Philip Wong <https://pwong.co.uk>
# Copyright © 2019 Joseph Lorimer <joseph@lorimer.me>
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

from os.path import dirname, join, realpath
from re import match


def get_frequency(hanzi):
    levels = [
        (200, 'very basic'),
        (100, 'basic'),
        (50, 'very common'),
        (25, 'common'),
        (13, 'uncommon'),
        (7, 'rare'),
        (2, 'very rare'),
        (0, 'obscure'),
    ]

    corpus_path = join(
        dirname(realpath(__file__)), 'data', 'freq', 'internet-zh'
    )

    found = False

    with open(corpus_path, encoding='utf8') as f:
        for line in f:
            res = match('[0-9]+ ([0-9.]+) %s$' % hanzi, line)
            if res:
                freq = float(res.group(1))
                found = True
                break

    html = '<div class="freq freq-unknown">unknown</div>'

    if not found:
        return html

    for level, desc in levels:
        if freq > level:
            html = '<div class="freq freq-%s">%s</div>' % (
                desc.replace(' ', '-'),
                desc,
            )
            break

    return html
