# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from aqt import mw
from aqt.qt import QAction
from aqt.utils import showInfo, openLink, askUser

from . import edit_behavior
from .about import CSR_GITHUB_URL, showAbout
from .config import chinese_support_config
from .fill_missing import (fill_pinyin,
                           fill_silhouette,
                           fill_simp_trad,
                           fill_sounds,
                           fill_translation)


ui_actions = {}

dictionaries = [
    ('None', _('None')),
    ('local_de', _('German')),
    ('local_en', _('English')),
    ('local_fr', _('French')),
]

transcriptions = ['Pinyin', 'Pinyin (Taiwan)', 'Cantonese', 'Bopomofo']

speech_options = [
    'None',
    'Baidu Translate',
    'Google Mandarin (PRC)',
    'Google Mandarin (Taiwan)',
]


def display_next_tip():
    (tip, link) = chinese_support_config.get_next_tip()
    if tip:
        if link:
            if askUser(tip):
                openLink(link)
        else:
            showInfo(tip)


def set_dict_constructor(dict):
    def set_dict():
        chinese_support_config.set_option('dictionary', dict)
        update_dict_action_checkboxes()
    return set_dict


def set_option_constructor(option, value):
    def set_option():
        chinese_support_config.set_option(option, value)
        update_dict_action_checkboxes()
    return set_option


def add_action(title, to, funct, checkable=False):
    action = QAction(_(title), mw)
    if checkable:
        action.setCheckable(True)
    action.triggered.connect(funct)
    to.addAction(action)
    return action


def update_dict_action_checkboxes():
    global ui_actions

    for d, d_name in dictionaries:
        ui_actions['dict_' + d].setChecked(
            d == chinese_support_config.options['dictionary'])

    for t in transcriptions:
        ui_actions['transcription_' + t].setChecked(
            t == chinese_support_config.options['transcription'])

    for t in speech_options:
        ui_actions['speech_' + t].setChecked(
            t == chinese_support_config.options['speech'])


def loadMenu():
    global ui_actions

    menu = mw.form.menuTools.addMenu('Chinese Support')

    submenu = menu.addMenu(_('Use local dictionary'))
    for d, d_names in dictionaries:
        ui_actions['dict_' + d] = add_action(
            d_names, submenu, set_dict_constructor(d), True)

    submenu = menu.addMenu(_('Set transcription'))
    for i in transcriptions:
        ui_actions['transcription_' + i] = add_action(
            i, submenu, set_option_constructor('transcription', i), True)

    submenu = menu.addMenu(_('Set speech engine'))
    for i in speech_options:
        ui_actions['speech_' + i] = add_action(
            i, submenu, set_option_constructor('speech', i), True)

    submenu = menu.addMenu(_('Fill incomplete notes'))
    add_action(_('Fill missing sounds'), submenu, fill_sounds)
    add_action(_('Fill pinyin and color'), submenu, fill_pinyin)
    add_action(_('Fill translation'), submenu, fill_translation)
    add_action(_('Fill simplified/traditional'), submenu, fill_simp_trad)
    add_action(_('Fill silhouette'), submenu, fill_silhouette)

    submenu = menu.addMenu(_('Help'))
    add_action(_('Report a bug or make a feature request'),
               submenu,
               lambda: openLink(CSR_GITHUB_URL + '/issues'))

    add_action(_('About...'), menu, showAbout)

    update_dict_action_checkboxes()


display_next_tip()
