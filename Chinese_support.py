# -*- coding: utf-8 ; mode: python -*-

# Chinese support addon for Anki2
########################################################################
"""
A Plugin for the Anki2 Spaced Repition learning system,
<http://ankisrs.net/>

   Copyright © 2012 by Roland Sieker, <ospalh@gmail.com> 
   Copyright © 2012 by Thomas TEMPÉ, <thomas.tempe@alysse.org>

   Using parts of the Japanese plugin by Damien Elms.
   Using parts of cjklib and sqlalchemy (see respective directories)

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version, unless otherwise noted.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# You should not have to edit this file for normal usage.
# All config options are in the add-on menu.


import os, sys, os.path
from aqt import mw
from aqt.utils import isWin


#Add local copy of sqlalchemy to Python path, for cjklib to work.
addon_dir = mw.pm.addonFolder()
if isWin:
    addon_dir = addon_dir.encode(sys.getfilesystemencoding())
sys.path.insert(0, os.path.join(addon_dir, "chinese") )
#Import a few modules from the full Python distribution, 
#which don't come with Anki on Windows or MacOS but are needed for cjklib
sys.path.append( os.path.join(addon_dir, "chinese", "python-2.7-modules") )

#Quick-and-dirty trick to remove cjklib warning on a Linux with a full
#python install, about having 2 different versions of sqlalchemy
while '/usr/lib/python2.7/dist-packages' in sys.path:
    i = sys.path.index('/usr/lib/python2.7/dist-packages')
    sys.path.pop(i)


#Create edit_behavior.py
edit_behavior_filename = os.path.join(addon_dir, "chinese", "edit_behavior.py")
edit_behavior_model = os.path.join(addon_dir, "chinese", "edit_behavior_model.py")

if not os.path.exists(edit_behavior_filename):
    open(edit_behavior_filename, "w").write(open(edit_behavior_model).read())
    import chinese.edit_behavior


import chinese.templates.ruby ; chinese.templates.ruby.install()
import chinese.templates.chinese ; chinese.templates.chinese.install()

from chinese.config import chinese_support_config
import chinese.edit
import chinese.models.compatibility
import chinese.models.ruby
import chinese.models.ruby_synonyms
import chinese.ui

    
