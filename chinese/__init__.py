# -*- coding: utf-8 -*-
# Chinese Support Redux; an add-on for Anki <http://ankisrs.net/>

# Copyright 2012 Roland Sieker <ospalh@gmail.com>
# Copyright 2012 Thomas Tempé <thomas.tempe@alysse.org>
# Copyright 2017 Joseph Lorimer <luoliyan@posteo.net>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from anki.hooks import addHook

from . import edit
from . import graph
from .models import advanced
from .models import basic
from .templates import chinese
from .templates import ruby
from .ui import loadMenu
# import chinese.models.compatibility
# import chinese.models.ruby
# import chinese.models.ruby_synonyms

ruby.install()
chinese.install()

addHook('profileLoaded', loadMenu)
