# Copyright © 2012 Roland Sieker <ospalh@gmail.com>
# Copyright © 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2019 Joseph Lorimer <joseph@lorimer.me>
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

from collections import defaultdict
from json import dump, load
from os.path import dirname, exists, join, realpath

from aqt import mw


class ConfigManager:
    default_path = join(dirname(realpath(__file__)), 'config.json')
    saved_path = join(dirname(realpath(__file__)), 'config_saved.json')

    with open(default_path, encoding='utf-8') as f:
        config = defaultdict(str, load(f))

    if exists(saved_path):
        with open(saved_path, encoding='utf-8') as f:
            config_saved = defaultdict(str, load(f))
        if config_saved['version'] == config['version']:
            config = config_saved

    def __setitem__(self, key, value):
        self.config[key] = value

    def __getitem__(self, key):
        return self.config[key]

    def update(self, d):
        self.config.update(d)

    def save(self):
        with open(self.saved_path, 'w', encoding='utf-8') as f:
            dump(self.config, f)
        mw.addonManager.writeConfig(__name__, self.config)

    def get_fields(self, groups=None):
        if not groups:
            groups = list(self.config['fields'])
        fields = []
        for g in groups:
            if g in self.config['fields']:
                fields.extend(self.config['fields'][g])
        return fields
