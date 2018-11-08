# Copyright © 2012 Roland Sieker <ospalh@gmail.com>
# Copyright © 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
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

from anki.hooks import addHook
from aqt import mw


class ConfigManager:
    def __init__(self):
        self.tips = []
        self.config = mw.addonManager.getConfig(__name__)
        addHook('unloadProfile', self.save)

    def __setitem__(self, key, value):
        self.config[key] = value

    def __getitem__(self, key):
        return self.config[key]

    def update(self, d):
        self.config.update(d)

    def save(self):
        try:
            mw.addonManager.writeConfig(__name__, self.config)
        except FileNotFoundError as e:
            print(e)

    def get_tip(self):
        if self.config['tip_number'] < len(self.tips):
            self.config['tip_number'] += 1
            return self.tips[self.config['tip_number'] - 1]
        return (None, None)
