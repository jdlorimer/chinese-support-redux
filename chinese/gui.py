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

from functools import partial

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QAction, QActionGroup, QMenu, QSpinBox

from aqt import mw
from aqt.utils import showInfo, openLink, askUser

from .about import CSR_GITHUB_URL, showAbout
from .fill import (
    fill_pinyin,
    fill_silhouette,
    fill_simp_trad,
    fill_sounds,
    fill_translation
)
from .main import config_manager


dictionaries = [
    ('None', _('None')),
    ('local_de', _('German')),
    ('local_en', _('English')),
    ('local_fr', _('French')),
]

transcriptions = [
    'Pinyin',
    'Pinyin (Taiwan)',
    'Cantonese',
    'Bopomofo',
]

speech_engines = [
    'None',
    'Baidu Translate',
    'Google Mandarin (PRC)',
    'Google Mandarin (Taiwan)',
]


def load_menu():
    for d, name in dictionaries:
        add_menu_item(
            'Chinese::Set Dictionary',
            name,
            partial(config_manager.options.update, {'dictionary': d}),
            checkable=True,
            checked=bool(config_manager.options['dictionary'] == d)
        )

    for t in transcriptions:
        add_menu_item(
            'Chinese::Set Transcription',
            t,
            partial(config_manager.options.update, {'transcription': t}),
            checkable=True,
            checked=bool(config_manager.options['transcription'] == t)
        )

    for s in speech_engines:
        add_menu_item(
            'Chinese::Set Speech Engine',
            s,
            partial(config_manager.options.update, {'speech': s}),
            checkable=True,
            checked=bool(config_manager.options['speech'] == s)
        )

    add_menu('Chinese::Fill Notes')
    add_menu_item(
        'Chinese::Fill Notes',
        _('Fill Sounds'),
        fill_sounds
    )
    add_menu_item(
        'Chinese::Fill Notes',
        _('Fill Transcription and Color'),
        fill_pinyin
    )
    add_menu_item(
        'Chinese::Fill Notes',
        _('Fill Translation'),
        fill_translation
    )
    add_menu_item(
        'Chinese::Fill Notes',
        _('Fill Characters'),
        fill_simp_trad
    )
    add_menu_item(
        'Chinese::Fill Notes',
        _('Fill Silhouette'),
        fill_silhouette
    )

    add_menu('Chinese::Help')
    add_menu_item(
        'Chinese::Help',
        _('Report a bug or make a feature request'),
        lambda: openLink(CSR_GITHUB_URL + '/issues')
    )
    add_menu_item('Chinese::Help', _('About...'), showAbout)


def unload_menu():
    for menu in mw.custom_menus.values():
        mw.form.menubar.removeAction(menu.menuAction())

    mw.custom_menus.clear()


def display_tip():
    (tip, link) = config_manager.get_next_tip()
    if tip:
        if link:
            if askUser(tip):
                openLink(link)
        else:
            showInfo(tip)


def add_menu(path):
    if not hasattr(mw, 'custom_menus'):
        mw.custom_menus = {}

    if len(path.split('::')) == 2:
        parent_path, child_path = path.split('::')
        has_child = True
    else:
        parent_path = path
        has_child = False

    if parent_path not in mw.custom_menus:
        parent = QMenu('&' + parent_path, mw)
        mw.custom_menus[parent_path] = parent
        mw.form.menubar.insertMenu(mw.form.menuTools.menuAction(), parent)

    if has_child and (path not in mw.custom_menus):
        child = QMenu('&' + child_path, mw)
        mw.custom_menus[path] = child
        mw.custom_menus[parent_path].addMenu(child)


def toggle_menu_vis(path):
    if path not in mw.custom_menus:
        return

    if mw.custom_menus[path].isEmpty():
        mw.custom_menus[path].menuAction().setVisible(False)
    else:
        mw.custom_menus[path].menuAction().setVisible(True)


def add_menu_item(path, text, func, keys=None, checkable=False, checked=False):
    action = QAction(text, mw)

    if keys:
        action.setShortcut(QKeySequence(keys))

    if checkable:
        action.setCheckable(checkable)
        action.toggled.connect(func)
        if not hasattr(mw, 'action_groups'):
            mw.action_groups = {}
        if path not in mw.action_groups:
            mw.action_groups[path] = QActionGroup(None)
        mw.action_groups[path].addAction(action)
        action.setChecked(checked)
    else:
        action.triggered.connect(func)

    if path == 'File':
        mw.form.menuCol.addAction(action)
    elif path == 'Edit':
        mw.form.menuEdit.addAction(action)
    elif path == 'Tools':
        mw.form.menuTools.addAction(action)
    elif path == 'Help':
        mw.form.menuHelp.addAction(action)
    else:
        add_menu(path)
        mw.custom_menus[path].addAction(action)
