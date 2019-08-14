# Copyright © 2012 Roland Sieker <ospalh@gmail.com>
# Copyright © 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2018 Joseph Lorimer <joseph@lorimer.me>
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
from json import load
from os.path import dirname, join, realpath
from typing import List

from aqt import mw


class ConfigManager:
    config_path = join(dirname(realpath(__file__)), 'config.json')
    config_saved = defaultdict(str, mw.addonManager.getConfig(__name__))

    with open(config_path, encoding='utf-8') as f:
        config_default = defaultdict(str, load(f))

    if config_saved['version'] == config_default['version']:
        config = config_saved
    else:
        config = config_default

    def __setitem__(self, key, value):
        self.config[key] = value

    def __getitem__(self, key):
        return self.config[key]

    def update(self, d) -> None:
        self.config.update(d)

    def save(self) -> None:
        mw.addonManager.writeConfig(__name__, self.config)

    def get_fields(self, groups: List[str] = []) -> List[str]:
        if not groups:
            groups = list(self.config['fields'])
        fields: List[str] = []
        for g in groups:
            fields.extend(self.config['fields'][g])
        return fields
